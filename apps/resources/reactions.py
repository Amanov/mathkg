"""Face reactions: one count per visitor and page, plus the topic material."""
import hashlib
import logging
import re
import secrets

from django.db import IntegrityError, transaction
from django.db.models import F
from django.db.models.signals import pre_delete
from django.urls import Resolver404, resolve
from django.utils import timezone

from apps.resources.models import (
    PageReaction,
    PageReactionCount,
    SubSubtopic,
    Subtopic,
    Topic,
)

logger = logging.getLogger(__name__)

VISITOR_COOKIE = 'mk_vid'
VOTED_COOKIE = 'mk_rx'
COOKIE_AGE = 60 * 60 * 24 * 400
VISITOR_RE = re.compile(r'^[a-f0-9]{32}$')

# Fixed site pages. A reaction on these stores the path only.
NON_TOPIC_URL_NAMES = {
    'home',
    'home_root',
    'about',
    'news_list',
    'pricing',
    'topics_tree',
    'feedback',
    'teacher_comments',
    'search',
    'resources',
    'login',
    'logout',
    'register',
    'account',
    'dashboard',
    'analytics_dashboard',
    'password_reset',
    'password_reset_done',
    'password_reset_confirm',
    'password_reset_complete',
    'password_change',
    'password_change_done',
}

# Endpoints that resolve but are not pages a teacher is reacting to.
BLOCKED_URL_NAMES = {
    'page_reaction',
    'track_click',
    'menu_fragment',
    'download_resource',
    'search_suggest',
    'robots_txt',
    'sitemap',
    'tarsia_builder_export',
}

FACE_FIELDS = {
    PageReaction.FACE_HAPPY: 'happy_count',
    PageReaction.FACE_OK: 'ok_count',
    PageReaction.FACE_SAD: 'sad_count',
}


def path_token(path):
    return hashlib.sha256(path.encode('utf-8')).hexdigest()[:12]


def visitor_key(request):
    key = request.COOKIES.get(VISITOR_COOKIE, '')
    if VISITOR_RE.fullmatch(key or ''):
        return key
    return secrets.token_hex(16)


def already_voted(request, path):
    raw = request.COOKIES.get(VOTED_COOKIE, '')
    return path_token(path) in raw.split('.')


def remember_vote(response, request, visitor, path):
    secure = request.is_secure()
    response.set_cookie(
        VISITOR_COOKIE,
        visitor,
        max_age=COOKIE_AGE,
        httponly=True,
        samesite='Lax',
        secure=secure,
    )
    token = path_token(path)
    tokens = [part for part in request.COOKIES.get(VOTED_COOKIE, '').split('.') if part]
    if token not in tokens:
        tokens.append(token)
    response.set_cookie(
        VOTED_COOKIE,
        '.'.join(tokens[-120:]),
        max_age=COOKIE_AGE,
        httponly=True,
        samesite='Lax',
        secure=secure,
    )
    return response


def clean_public_path(raw):
    """A real page path on this site, or None."""
    path = (raw or '').strip().split('?', 1)[0].split('#', 1)[0]
    if not path.startswith('/') or path.startswith('//'):
        return None
    if '\\' in path or '..' in path or '\x00' in path or len(path) > 255:
        return None
    try:
        match = resolve(path)
    except Resolver404:
        return None
    if match.namespace == 'admin' or match.url_name in BLOCKED_URL_NAMES:
        return None
    return path


def material_for_path(path):
    """Topic, subtopic, and the material title when this path is a topic page."""
    info = {
        'topic': None,
        'subtopic': None,
        'subsubtopic': None,
        'material': '',
    }
    try:
        match = resolve(path)
    except Resolver404:
        return info
    if match.url_name in NON_TOPIC_URL_NAMES:
        return info

    kwargs = match.kwargs
    topic_slug = kwargs.get('topic_slug')
    if topic_slug:
        topic = Topic.objects.filter(slug=topic_slug).first()
        info['topic'] = topic
        if topic:
            info['material'] = topic.title
        subtopic_slug = kwargs.get('subtopic_slug')
        if topic and subtopic_slug:
            subtopic = Subtopic.objects.filter(topic=topic, slug=subtopic_slug).first()
            info['subtopic'] = subtopic
            if subtopic:
                info['material'] = subtopic.title
            subsub_slug = kwargs.get('subsubtopic_slug')
            if subtopic and subsub_slug:
                subsub = SubSubtopic.objects.filter(
                    subtopic=subtopic, slug=subsub_slug,
                ).first()
                info['subsubtopic'] = subsub
                if subsub:
                    info['material'] = subsub.title

    if not info['material']:
        info['material'] = _catalog_title(path)
    info['material'] = (info['material'] or '')[:255]
    return info


def _catalog_title(path):
    """Title of a hand-built topic page. Empty when the path is not one.

    This stays off the search catalog. Building that catalog reads the
    grade table and every pack, which is the wrong cost for one tap.
    """
    norm = path if path.endswith('/') or path == '/' else path + '/'
    try:
        from apps.resources.grade_search import _hand_built
        spec = _hand_built().get(norm) or {}
        if spec.get('title'):
            return spec['title']
    except Exception:
        logger.exception('Could not read a hand-built topic title')

    slug = norm.strip('/')
    if slug and '/' not in slug:
        try:
            from apps.resources.views.onduktar_placeholders import (
                OPERATION_PLACEHOLDER_TITLES,
            )
            title = OPERATION_PLACEHOLDER_TITLES.get(slug)
            if title:
                return title
        except Exception:
            logger.exception('Could not read a placeholder topic title')
        try:
            from apps.resources.grade_search import _bridge_meta
            _crumbs, titles = _bridge_meta()
            if titles.get(norm):
                return titles[norm]
        except Exception:
            logger.exception('Could not read a bridge topic title')
    return ''


def _bump_count(path, face, material):
    field = FACE_FIELDS[face]
    defaults = {
        'material': material,
        'happy_count': 1 if face == PageReaction.FACE_HAPPY else 0,
        'ok_count': 1 if face == PageReaction.FACE_OK else 0,
        'sad_count': 1 if face == PageReaction.FACE_SAD else 0,
    }
    row, created = PageReactionCount.objects.get_or_create(path=path, defaults=defaults)
    if created:
        return
    updates = {field: F(field) + 1, 'updated_at': timezone.now()}
    if material:
        updates['material'] = material
    PageReactionCount.objects.filter(pk=row.pk).update(**updates)


def release_reaction(reaction):
    """Drop one face from the per-page totals when a vote is removed."""
    field = FACE_FIELDS.get(reaction.face)
    if not field:
        return
    row = PageReactionCount.objects.filter(path=reaction.path).first()
    if row is None:
        return
    PageReactionCount.objects.filter(pk=row.pk, **{f'{field}__gt': 0}).update(
        **{field: F(field) - 1, 'updated_at': timezone.now()}
    )


def _release_on_delete(sender, instance, **kwargs):
    release_reaction(instance)


def connect_signals():
    pre_delete.connect(
        _release_on_delete,
        sender=PageReaction,
        dispatch_uid='page_reaction_release',
    )


def record_reaction(path, face, visitor):
    """Save one new face. False when this visitor already counted for the page."""
    if face not in FACE_FIELDS:
        raise ValueError(face)
    info = material_for_path(path)
    try:
        with transaction.atomic():
            PageReaction.objects.create(
                path=path,
                face=face,
                material=info['material'],
                topic=info['topic'],
                subtopic=info['subtopic'],
                subsubtopic=info['subsubtopic'],
                visitor_key=visitor,
            )
            _bump_count(path, face, info['material'])
    except IntegrityError:
        return False
    return True
