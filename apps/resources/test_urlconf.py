"""Every public route from before the URLconf split still resolves.

The snapshot was taken from config/urls.py on main after the media
allowlist, and before these routes moved into per-section modules. The
only intentional difference is the duplicate name ``home``: ``/`` is now
``home_root``, and ``home`` stays on ``/home/`` so existing
{% url 'home' %} links do not change. /media/ still goes through the
allowlist view, not a catch-all.
"""
import json
import os
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase, TestCase
from django.urls import get_resolver, reverse, resolve

from apps.resources.views import home_screen_view
from config.media_views import public_media

SNAPSHOT_PATH = Path(__file__).resolve().parent / 'url_patterns_snapshot.json'

SAMPLES = {
    'IntConverter': 1,
    'SlugConverter': 'sample-slug',
    'StringConverter': 'sample',
    'PathConverter': 'sample/path',
    'UUIDConverter': '12345678-1234-5678-1234-567812345678',
}


def _normalize_default(value):
    if isinstance(value, os.PathLike):
        value = os.fspath(value)
    if isinstance(value, str):
        base = str(settings.BASE_DIR)
        if value == base or value.startswith(base + os.sep):
            rel = value[len(base):].lstrip('/\\').replace('\\', '/')
            return 'BASE/' + rel
    return value


def flatten_urlpatterns(resolver=None, prefix='', namespace=''):
    if resolver is None:
        resolver = get_resolver()
        namespace = resolver.namespace or ''
    rows = []
    for pattern in resolver.url_patterns:
        if hasattr(pattern, 'url_patterns'):
            child_ns = pattern.namespace if pattern.namespace is not None else namespace
            rows.extend(flatten_urlpatterns(
                pattern, prefix + str(pattern.pattern), child_ns,
            ))
            continue
        rows.append({
            'namespace': namespace,
            'pattern': prefix + str(pattern.pattern),
            'name': pattern.name,
            'defaults': {
                key: _normalize_default(val)
                for key, val in (pattern.default_args or {}).items()
            },
            'callback': pattern.lookup_str,
        })
    return rows


def _expected_patterns():
    snapshot = json.loads(SNAPSHOT_PATH.read_text())
    expected = []
    for row in snapshot['patterns']:
        row = dict(row)
        if row['namespace'] == '' and row['pattern'] == '' and row['name'] == 'home':
            row['name'] = 'home_root'
        expected.append(row)
    return snapshot, expected


class UrlSnapshotTests(SimpleTestCase):
    def test_every_pattern_matches_the_pre_split_snapshot(self):
        _snapshot, expected = _expected_patterns()
        got = flatten_urlpatterns()
        diffs = []
        if len(got) != len(expected):
            diffs.append(f'length {len(expected)} -> {len(got)}')
        for index, (before, after) in enumerate(zip(expected, got)):
            if before != after:
                diffs.append(f'{index}: {before} -> {after}')
            if len(diffs) >= 8:
                break
        self.assertEqual(diffs, [])

    def test_every_named_route_still_reverses_to_the_same_path(self):
        snapshot, _expected = _expected_patterns()
        mismatches = []
        for item in snapshot['reversals']:
            try:
                path = reverse(item['name'], kwargs=item['kwargs'])
            except Exception as exc:
                mismatches.append(f"{item['name']}: {exc}")
                continue
            if path != item['path']:
                mismatches.append(f"{item['name']}: {item['path']} -> {path}")
            if len(mismatches) >= 8:
                break
        self.assertEqual(mismatches, [])

    def test_home_name_points_at_the_home_alias_and_root_still_renders_home(self):
        self.assertEqual(reverse('home'), '/home/')
        self.assertEqual(reverse('home_root'), '/')
        self.assertIs(resolve('/').func, home_screen_view)
        self.assertIs(resolve('/home/').func, home_screen_view)
        names = [
            row['name']
            for row in flatten_urlpatterns()
            if row['namespace'] == '' and row['pattern'] in ('', 'home/')
        ]
        self.assertEqual(names, ['home_root', 'home'])

    def test_media_route_uses_the_allowlist(self):
        media = [
            row for row in flatten_urlpatterns()
            if 'media/' in row['pattern']
        ]
        self.assertEqual(len(media), 1)
        self.assertEqual(media[0]['pattern'], r'^media/(?P<path>.*)$')
        self.assertEqual(media[0]['callback'], 'config.media_views.public_media')
        self.assertIs(resolve('/media/resources/images/thumb.png').func, public_media)


class HomeRouteTests(TestCase):
    def test_root_and_home_alias_both_render(self):
        for path in ('/', '/home/'):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, path)
