"""Build a test paper from the question bank and render it as PDF.

Questions are never invented here. Every item is a published Question.
"""

import random
import re

from django import forms
from django.db import transaction
from django.utils import timezone

from apps.account.models import PLAN_ONE_YEAR, PLAN_SIX_MONTHS, PLAN_THREE_MONTHS
from apps.resources.models import GeneratedTest, Question, Topic

FREE_MONTHLY_LIMIT = 3
PAID_PLANS = {PLAN_THREE_MONTHS, PLAN_SIX_MONTHS, PLAN_ONE_YEAR}

_MIX_WEIGHTS = {
    GeneratedTest.MIX_EQUAL: (1, 1, 1),
    GeneratedTest.MIX_MOSTLY_EASY: (6, 3, 1),
    GeneratedTest.MIX_MOSTLY_MEDIUM: (2, 6, 2),
    GeneratedTest.MIX_MOSTLY_HARD: (1, 3, 6),
    GeneratedTest.MIX_EASY: (1, 0, 0),
    GeneratedTest.MIX_MEDIUM: (0, 1, 0),
    GeneratedTest.MIX_HARD: (0, 0, 1),
}
_DIFFICULTIES = (
    Question.DIFFICULTY_EASY,
    Question.DIFFICULTY_MEDIUM,
    Question.DIFFICULTY_HARD,
)


class NotEnoughQuestions(Exception):
    pass


class QuotaExceeded(Exception):
    pass


def single_grade_number(badge):
    """A single class number from a badge such as «5 кл.». Ranges stay blank."""
    nums = re.findall(r'\d+', badge or '')
    if len(nums) != 1:
        return ''
    number = int(nums[0])
    if 1 <= number <= 11:
        return str(number)
    return ''


def user_is_paid(user):
    return user.current_plan in PAID_PLANS and user.has_active_subscription


def month_start():
    now = timezone.localtime()
    return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def monthly_usage(user):
    used = GeneratedTest.objects.filter(
        user=user,
        created_at__gte=month_start(),
    ).count()
    if user_is_paid(user):
        return {
            'paid': True,
            'limit': None,
            'used': used,
            'remaining': None,
            'allowed': True,
        }
    remaining = max(0, FREE_MONTHLY_LIMIT - used)
    return {
        'paid': False,
        'limit': FREE_MONTHLY_LIMIT,
        'used': used,
        'remaining': remaining,
        'allowed': remaining > 0,
    }


TOPIC_KEY_PREFIX = 'tema-'
# Same order as the site menu.
AREA_ORDER = ('number', 'proportion', 'algebra', 'geometry', 'probability', 'statistics')


def theme_key(question):
    """The choice a teacher ticks: the pack («Бөлүм») or, for older rows, the topic."""
    return question.theme_slug or TOPIC_KEY_PREFIX + question.topic.slug


def theme_title(question):
    return question.theme or question.topic.title


class ThemeStats(dict):
    """theme key -> {grade: published question count}.

    ``info[key]`` keeps the title, the area topic and its order.
    """

    def __init__(self):
        super().__init__()
        self.info = {}


def published_topic_stats():
    stats = ThemeStats()
    rows = Question.objects.filter(is_published=True).values_list(
        'theme_slug', 'theme', 'topic_id', 'topic__slug', 'topic__title', 'topic__order', 'grade',
    )
    for slug, title, topic_id, topic_slug, topic_title, topic_order, grade in rows:
        key = slug or TOPIC_KEY_PREFIX + topic_slug
        bucket = stats.setdefault(key, {})
        bucket[grade] = bucket.get(grade, 0) + 1
        if key not in stats.info:
            stats.info[key] = {
                'title': title or topic_title,
                'topic_id': topic_id,
                'area': topic_slug,
                'area_title': topic_title,
                'order': (
                    topic_order,
                    AREA_ORDER.index(topic_slug) if topic_slug in AREA_ORDER else len(AREA_ORDER),
                    title or topic_title,
                ),
            }
    return stats


def available_grades(stats):
    grades = {grade for counts in stats.values() for grade in counts}
    return sorted(grades) or [5, 6]


def _theme_filter(keys):
    from django.db.models import Q

    themes = [key for key in keys if not key.startswith(TOPIC_KEY_PREFIX)]
    topics = [key[len(TOPIC_KEY_PREFIX):] for key in keys if key.startswith(TOPIC_KEY_PREFIX)]
    return Q(theme_slug__in=themes) | Q(theme_slug='', topic__slug__in=topics)


def difficulty_quotas(count, mix):
    weights = _MIX_WEIGHTS[mix]
    total = sum(weights)
    if total == 0 or count < 1:
        raise ValueError(mix)
    raw = [count * weight / total for weight in weights]
    floors = [int(value) for value in raw]
    leftover = count - sum(floors)
    order = sorted(
        range(len(weights)),
        key=lambda index: (raw[index] - floors[index], -index),
        reverse=True,
    )
    for index in order[:leftover]:
        floors[index] += 1
    return dict(zip(_DIFFICULTIES, floors))


def _fill_order(mix):
    if mix in (GeneratedTest.MIX_EASY, GeneratedTest.MIX_MOSTLY_EASY):
        return _DIFFICULTIES
    if mix in (GeneratedTest.MIX_HARD, GeneratedTest.MIX_MOSTLY_HARD):
        return (
            Question.DIFFICULTY_HARD,
            Question.DIFFICULTY_MEDIUM,
            Question.DIFFICULTY_EASY,
        )
    return (
        Question.DIFFICULTY_MEDIUM,
        Question.DIFFICULTY_EASY,
        Question.DIFFICULTY_HARD,
    )


def _not_enough_message(have, need):
    return (
        f'Тандалган түр, класс жана темалар боюнча жарыяланган суроо {have} гана. '
        f'{need} суроо сурадыңыз. Санды азайтыңыз же тема кошуңуз.'
    )


def _reserve_one_per_format(questions, count, rng):
    """Keep one item of each format when the paper mixes several formats."""
    formats = []
    for question in questions:
        if question.question_format not in formats:
            formats.append(question.question_format)
    if len(formats) < 2:
        return []
    reserved = []
    used = set()
    for fmt in formats:
        if len(reserved) >= count:
            break
        bucket = [
            row for row in questions
            if row.question_format == fmt and row.pk not in used
        ]
        if not bucket:
            continue
        rng.shuffle(bucket)
        reserved.append(bucket[0])
        used.add(bucket[0].pk)
    return reserved


def assemble_variants(questions, *, mix, question_count, variant_count, rng):
    """Return (variants, borrowed).

    Each variant is a list of Question rows. No question is repeated
    inside one variant. Variants may share questions when the bank is small.
    When several formats are in the pool, each variant includes one of each
    before the level mix fills the rest.
    """
    questions = list(questions)
    if len(questions) < question_count:
        raise NotEnoughQuestions(_not_enough_message(len(questions), question_count))

    variants = []
    borrowed = False
    for _ in range(variant_count):
        reserved = _reserve_one_per_format(questions, question_count, rng)
        reserved_ids = {row.pk for row in reserved}
        need = question_count - len(reserved)
        chosen = list(reserved)
        did_borrow = False
        if need:
            rest = [row for row in questions if row.pk not in reserved_ids]
            quotas = difficulty_quotas(need, mix)
            grouped = {key: [] for key in _DIFFICULTIES}
            for question in rest:
                grouped[question.difficulty].append(question)
            more, did_borrow = _pick_variant(grouped, quotas, mix, rng)
            chosen.extend(more)
        rng.shuffle(chosen)
        variants.append(chosen)
        borrowed = borrowed or did_borrow
    return variants, borrowed


def _pick_variant(grouped, quotas, mix, rng):
    chosen = []
    used = set()
    shortfall = 0
    for difficulty in _DIFFICULTIES:
        bucket = [row for row in grouped[difficulty] if row.pk not in used]
        rng.shuffle(bucket)
        need = quotas[difficulty]
        take = bucket[:need]
        chosen.extend(take)
        used.update(row.pk for row in take)
        shortfall += need - len(take)

    borrowed = False
    if shortfall:
        rest = []
        for difficulty in _fill_order(mix):
            bucket = [row for row in grouped[difficulty] if row.pk not in used]
            rng.shuffle(bucket)
            rest.extend(bucket)
        chosen.extend(rest[:shortfall])
        borrowed = True
    rng.shuffle(chosen)
    return chosen, borrowed


_LINE_COUNTS = {
    Question.FORMAT_EXTENDED: 4,
    Question.FORMAT_WRITTEN: 4,
    Question.FORMAT_SHORT: 2,
    Question.FORMAT_CALCULATION: 2,
    Question.FORMAT_DIAGRAM: 2,
    Question.FORMAT_FILL_BLANK: 1,
}


def _question_payload(question, number):
    fmt = question.question_format
    stored = question.options or {}
    options = []
    left = []
    right = []
    if fmt == Question.FORMAT_MATCHING:
        left = [{'n': key, 'text': stored.get('left', {})[key]} for key in stored.get('left', {})]
        right = [
            {'letter': key, 'text': stored.get('right', {})[key]}
            for key in stored.get('right', {})
        ]
    elif fmt in (Question.FORMAT_CHOICE, Question.FORMAT_TRUE_FALSE):
        letters = Question.OPTION_LETTERS if fmt == Question.FORMAT_CHOICE else ('А', 'Б')
        for letter in letters:
            if str(stored.get(letter, '')).strip():
                options.append({'letter': letter, 'text': stored[letter]})
    line_count = _LINE_COUNTS.get(fmt, 0)
    return {
        'id': question.pk,
        'number': number,
        'text': question.text,
        'format': fmt,
        'type': question.question_type,
        'type_label': question.get_question_format_display(),
        'options': options,
        'left': left,
        'right': right,
        'figure': fmt == Question.FORMAT_DIAGRAM,
        'line_slots': list(range(line_count)),
        'answer': question.answer,
        'solution': question.solution or '',
        'points': question.points,
        'minutes': question.estimated_minutes or 1,
        'difficulty': question.difficulty,
        'difficulty_label': question.get_difficulty_display(),
        'topic': theme_title(question),
        'is_sample': question.is_sample,
    }


def formats_label(formats):
    labels = dict(Question.FORMAT_CHOICES)
    return ', '.join(labels[item] for item in formats if item in labels)


def levels_label(levels):
    labels = dict(Question.DIFFICULTY_CHOICES)
    return ', '.join(labels[item] for item in levels if item in labels)


def _minutes(question):
    return question.estimated_minutes or 1


def choose_for_duration(questions, target_minutes, rng):
    """A subset whose minutes land as close as possible to the target.

    When several formats are available, one of each is kept if that still
    fits. Returns (questions, total_minutes).
    """
    pool = list(questions)
    if not pool:
        raise NotEnoughQuestions(
            'Тандалган класс, тема, түр жана деңгээл боюнча суроо жок.'
        )
    by_format = []
    for question in pool:
        if question.question_format not in by_format:
            by_format.append(question.question_format)
    reserved = []
    used = set()
    for fmt in by_format:
        bucket = [row for row in pool if row.question_format == fmt and row.pk not in used]
        rng.shuffle(bucket)
        bucket.sort(key=_minutes)
        reserved.append(bucket[0])
        used.add(bucket[0].pk)
    while len(reserved) > 1 and sum(_minutes(row) for row in reserved) > target_minutes:
        reserved.sort(key=_minutes)
        dropped = reserved.pop()
        used.discard(dropped.pk)
    chosen = list(reserved)
    rest = [row for row in pool if row.pk not in used]
    rng.shuffle(rest)
    while rest:
        current = sum(_minutes(row) for row in chosen)
        best = None
        best_distance = abs(current - target_minutes)
        for row in rest:
            distance = abs(current + _minutes(row) - target_minutes)
            if distance < best_distance:
                best = row
                best_distance = distance
        if best is None:
            break
        chosen.append(best)
        rest.remove(best)
    rng.shuffle(chosen)
    return chosen, sum(_minutes(row) for row in chosen)


def build_payload(
    questions, *, grade, test_type, formats, levels, duration_minutes,
    variant_count, show_timer=False, title='', rng=None,
):
    rng = rng or random.Random()
    packed = []
    planned = 0
    for index in range(1, variant_count + 1):
        rows, planned = choose_for_duration(questions, duration_minutes, rng)
        items = [_question_payload(row, number) for number, row in enumerate(rows, start=1)]
        packed.append({
            'number': index,
            'questions': items,
            'points': sum(item['points'] for item in items),
            'minutes': sum(item['minutes'] for item in items),
        })
    topic_titles = []
    for question in questions:
        if theme_title(question) not in topic_titles:
            topic_titles.append(theme_title(question))
    flat = [item for variant in packed for item in variant['questions']]
    return {
        'grade': grade,
        'grade_label': f'{grade}-класс',
        'test_type': test_type,
        'test_type_label': dict(GeneratedTest.TYPE_CHOICES)[test_type],
        'mix_label': levels_label(levels),
        'formats_label': formats_label(formats),
        'topics_label': ', '.join(topic_titles),
        'created_label': timezone.localdate().strftime('%d.%m.%Y'),
        'duration_minutes': duration_minutes,
        'planned_minutes': planned,
        'show_timer': show_timer,
        'title': (title or '').strip(),
        'variants': packed,
        'borrowed': False,
        'sample_only': bool(flat) and all(item['is_sample'] for item in flat),
        'duration_note': (
            f'Суралган убакыт {duration_minutes} мүнөт. '
            f'Тандалган суроолор болжолу {planned} мүнөт: '
            'мүмкүн болушунча жакын.'
        ),
        'marking_note': (
            'Ар бир суроого жазылган балл коюлат. Жооп ачкычындагы жооп '
            'менен дал келсе, толук балл коюлат. Жарым балл каралбайт.'
        ),
    }


def questions_for(grade, themes, formats, levels):
    return list(
        Question.objects.filter(
            _theme_filter(themes),
            is_published=True,
            grade=grade,
            question_format__in=formats,
            difficulty__in=levels,
        ).select_related('topic')
    )


def create_generated_test(user, cleaned, rng=None):
    formats = list(cleaned['formats'])
    levels = list(cleaned['levels'])
    questions = questions_for(cleaned['grade'], cleaned['topics'], formats, levels)
    payload = build_payload(
        questions,
        grade=cleaned['grade'],
        test_type=cleaned['test_type'],
        formats=formats,
        levels=levels,
        duration_minutes=cleaned['duration_minutes'],
        variant_count=cleaned['variant_count'],
        show_timer=cleaned.get('show_timer') or False,
        title=cleaned.get('title') or '',
        rng=rng,
    )
    with transaction.atomic():
        usage = monthly_usage(user)
        if not usage['allowed']:
            raise QuotaExceeded(
                'Бул айда 3 тест түзүлдү. Акысыз жана сыноо аккаунттары '
                'айына 3 тест түзө алат.'
            )
        generated = GeneratedTest.objects.create(
            user=user,
            grade=cleaned['grade'],
            test_type=cleaned['test_type'],
            question_count=len(payload['variants'][0]['questions']),
            variant_count=cleaned['variant_count'],
            formats=formats,
            levels=levels,
            duration_minutes=cleaned['duration_minutes'],
            show_timer=bool(cleaned.get('show_timer')),
            title=(cleaned.get('title') or '').strip(),
            payload=payload,
        )
        generated.topics.set({question.topic_id for question in questions})
    return generated


def render_test_pdf(payload):
    """PDF bytes for a paper; see test_pdf.py (PyMuPDF, no system libraries)."""
    from apps.resources.test_pdf import render_test_pdf as render

    return render(payload)


class TopicCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def __init__(self, attrs=None, choices=(), topic_stats=None):
        self.topic_stats = topic_stats or {}
        super().__init__(attrs, choices)

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs,
        )
        key = str(getattr(value, 'value', value))
        counts = self.topic_stats.get(key, {})
        info = getattr(self.topic_stats, 'info', {}).get(key)
        if info:
            option['attrs']['data-area'] = info['area_title']
        option['attrs']['data-counts'] = ','.join(
            f'{grade}:{count}' for grade, count in sorted(counts.items())
        )
        return option


class TestMakerForm(forms.Form):
    grade = forms.TypedChoiceField(
        coerce=int,
        choices=(),
        label='Класс',
        widget=forms.Select(attrs={'class': 'form-select'}),
        error_messages={'required': 'Класс тандаңыз.'},
    )
    topics = forms.MultipleChoiceField(
        choices=(),
        label='Темалар',
        widget=forms.CheckboxSelectMultiple,
        error_messages={'required': 'Кеминде бир теманы белгилеңиз.'},
    )
    test_type = forms.ChoiceField(
        choices=GeneratedTest.TYPE_CHOICES,
        label='Тесттин түрү',
        widget=forms.RadioSelect,
    )
    formats = forms.MultipleChoiceField(
        choices=Question.FORMAT_CHOICES,
        label='Суроолордун түрү',
        error_messages={'required': 'Кеминде бир түрдү тандаңыз.'},
        widget=forms.CheckboxSelectMultiple,
    )
    levels = forms.MultipleChoiceField(
        choices=Question.DIFFICULTY_CHOICES,
        label='Деңгээл',
        error_messages={'required': 'Кеминде бир деңгээлди тандаңыз.'},
        widget=forms.CheckboxSelectMultiple,
    )
    duration_minutes = forms.IntegerField(
        min_value=5,
        max_value=90,
        label='Тесттин узактыгы',
        widget=forms.NumberInput(attrs={
            'type': 'range',
            'min': 5,
            'max': 90,
            'step': 5,
            'id': 'id_duration_minutes',
        }),
        error_messages={
            'required': 'Убакытты тандаңыз.',
            'invalid': 'Убакытты мүнөт менен тандаңыз.',
            'min_value': 'Эң аз 5 мүнөт.',
            'max_value': 'Эң көп 90 мүнөт.',
        },
    )
    show_timer = forms.BooleanField(
        required=False,
        label='Убакытты көрсөтүү',
    )
    title = forms.CharField(
        required=False,
        max_length=120,
        label='Тесттин аты',
    )
    variant_count = forms.TypedChoiceField(
        coerce=int,
        choices=[(n, str(n)) for n in range(1, 5)],
        label='Варианттардын саны',
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, topic_stats=None, **kwargs):
        self.topic_stats = topic_stats or {}
        super().__init__(*args, **kwargs)
        grades = available_grades(self.topic_stats)
        self.fields['grade'].choices = [(grade, f'{grade}-класс') for grade in grades]
        info = getattr(self.topic_stats, 'info', {})
        keys = sorted(self.topic_stats, key=lambda key: info.get(key, {}).get('order', (0, 0, key)))
        self.fields['topics'].choices = [(key, info.get(key, {}).get('title', key)) for key in keys]
        # Replacing the widget after ChoiceField.__init__ drops the choices
        # the field already copied onto the previous widget.
        widget = TopicCheckboxSelectMultiple(topic_stats=self.topic_stats)
        widget.choices = self.fields['topics'].choices
        self.fields['topics'].widget = widget

    def clean(self):
        cleaned = super().clean()
        grade = cleaned.get('grade')
        topics = cleaned.get('topics')
        if grade and topics:
            info = getattr(self.topic_stats, 'info', {})
            missing = [
                info.get(key, {}).get('title', key) for key in topics
                if grade not in self.topic_stats.get(key, {})
            ]
            if missing:
                self.add_error(
                    'topics',
                    'Бул класс үчүн тандалган темада суроо жок: ' + ', '.join(missing) + '.',
                )
        minutes = cleaned.get('duration_minutes')
        if minutes is not None:
            snapped = int(round(minutes / 5.0) * 5)
            cleaned['duration_minutes'] = min(90, max(5, snapped))
        return cleaned


def initial_from_query(request, topic_stats):
    grades = available_grades(topic_stats)
    slugs = request.GET.getlist('tema')
    if not slugs and request.GET.get('tema'):
        slugs = [request.GET.get('tema')]
    info = getattr(topic_stats, 'info', {})
    topics = []
    for slug in slugs:
        if slug in topic_stats:
            topics.append(slug)
        elif TOPIC_KEY_PREFIX + slug in topic_stats:
            topics.append(TOPIC_KEY_PREFIX + slug)
        else:
            # An area link («Сандар») ticks every pack of that area.
            topics.extend(key for key in topic_stats if info.get(key, {}).get('area') == slug)
    raw_grade = request.GET.get('klass') or request.GET.get('grade')
    try:
        grade = int(raw_grade)
    except (TypeError, ValueError):
        grade = None
    if grade not in grades:
        grade = None
    if grade is None and topics:
        covered = set()
        for topic in topics:
            covered.update(topic_stats.get(topic, {}))
        for preferred in (5, 6):
            if preferred in covered and preferred in grades:
                grade = preferred
                break
        if grade is None and covered:
            grade = min(covered)
    if grade is None:
        grade = 5 if 5 in grades else grades[0]
    topics = [
        topic for topic in topics
        if grade in topic_stats.get(topic, {})
    ]
    return {
        'grade': grade,
        'topics': topics,
        'test_type': GeneratedTest.TYPE_FORMATIVE,
        'formats': [],
        'levels': [],
        'duration_minutes': 45,
        'show_timer': False,
        'variant_count': 1,
        'title': '',
    }
