"""Build a test paper from the question bank and render it as PDF.

Questions are never invented here. Every item is a published Question.
"""

import random
import re
from pathlib import Path

from django import forms
from django.conf import settings
from django.db import transaction
from django.template.loader import render_to_string
from django.utils import timezone

from apps.account.models import PLAN_ONE_YEAR, PLAN_SIX_MONTHS, PLAN_THREE_MONTHS
from apps.resources.models import GeneratedTest, Question, Topic

FREE_MONTHLY_LIMIT = 3
PAID_PLANS = {PLAN_THREE_MONTHS, PLAN_SIX_MONTHS, PLAN_ONE_YEAR}

_DEJAVU = Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
_DEJAVU_BOLD = Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
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


def published_topic_stats():
    """topic id -> {grade: published question count}."""
    stats = {}
    rows = Question.objects.filter(is_published=True).values_list('topic_id', 'grade')
    for topic_id, grade in rows:
        bucket = stats.setdefault(topic_id, {})
        bucket[grade] = bucket.get(grade, 0) + 1
    return stats


def available_grades(stats):
    grades = {grade for counts in stats.values() for grade in counts}
    return sorted(grades) or [5, 6]


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
        'answer': question.answer,
        'solution': question.solution or '',
        'points': question.points,
        'difficulty': question.difficulty,
        'difficulty_label': question.get_difficulty_display(),
        'topic': question.topic.title,
        'is_sample': question.is_sample,
    }


FORMAT_MODE_CHOICES = (
    ('choice', 'Тест (жооп тандоо)'),
    ('written', 'Классикалык (жазуу менен чыгаруу)'),
    ('mixed', 'Аралаш'),
)
EXTRA_FORMAT_CHOICES = (
    (Question.FORMAT_TRUE_FALSE, 'Туура/туура эмес'),
    (Question.FORMAT_MATCHING, 'Дал келтирүү'),
    (Question.FORMAT_FILL_BLANK, 'Боштукту толтуруу'),
)
BORROWED_NOTE = (
    'Кээ бир деңгээлде суроо жетпей калды. '
    'Жетишпеген орун башка деңгээлден толду.'
)


def selected_formats(mode, extras):
    selected = []
    if mode == 'written':
        selected.append(Question.FORMAT_WRITTEN)
    elif mode == 'mixed':
        selected.extend([Question.FORMAT_CHOICE, Question.FORMAT_WRITTEN])
    else:
        selected.append(Question.FORMAT_CHOICE)
    for extra in extras or []:
        if extra not in selected:
            selected.append(extra)
    return selected


def formats_label(mode, extras):
    label = dict(FORMAT_MODE_CHOICES)[mode]
    extra_labels = [dict(EXTRA_FORMAT_CHOICES)[item] for item in extras or []]
    if extra_labels:
        return label + ' · ' + ', '.join(extra_labels)
    return label


def build_payload(
    questions, *, grade, test_type, mix, question_count, variant_count,
    format_mode='mixed', extra_formats=None, rng=None,
):
    rng = rng or random.Random()
    variants, borrowed = assemble_variants(
        questions,
        mix=mix,
        question_count=question_count,
        variant_count=variant_count,
        rng=rng,
    )
    packed = []
    for index, rows in enumerate(variants, start=1):
        items = [_question_payload(row, number) for number, row in enumerate(rows, start=1)]
        packed.append({
            'number': index,
            'questions': items,
            'points': sum(item['points'] for item in items),
        })
    topic_titles = []
    for question in questions:
        if question.topic.title not in topic_titles:
            topic_titles.append(question.topic.title)
    flat = [item for variant in packed for item in variant['questions']]
    return {
        'grade': grade,
        'grade_label': f'{grade}-класс',
        'test_type': test_type,
        'test_type_label': dict(GeneratedTest.TYPE_CHOICES)[test_type],
        'mix': mix,
        'mix_label': dict(GeneratedTest.MIX_CHOICES)[mix],
        'formats_label': formats_label(format_mode, extra_formats),
        'topics_label': ', '.join(topic_titles),
        'created_label': timezone.localdate().strftime('%d.%m.%Y'),
        'variants': packed,
        'borrowed': borrowed,
        'sample_only': bool(flat) and all(item['is_sample'] for item in flat),
        'marking_note': (
            'Ар бир суроого жазылган балл коюлат. Жооп ачкычындагы жооп '
            'менен дал келсе, толук балл коюлат. Жарым балл каралбайт.'
        ),
    }


def questions_for(grade, topics, formats):
    return list(
        Question.objects.filter(
            is_published=True,
            grade=grade,
            topic__in=topics,
            question_format__in=formats,
        ).select_related('topic')
    )


def create_generated_test(user, cleaned, rng=None):
    extras = list(cleaned.get('extra_formats') or [])
    formats = selected_formats(cleaned['format_mode'], extras)
    questions = questions_for(cleaned['grade'], cleaned['topics'], formats)
    payload = build_payload(
        questions,
        grade=cleaned['grade'],
        test_type=cleaned['test_type'],
        mix=cleaned['difficulty_mix'],
        question_count=cleaned['question_count'],
        variant_count=cleaned['variant_count'],
        format_mode=cleaned['format_mode'],
        extra_formats=extras,
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
            question_count=cleaned['question_count'],
            variant_count=cleaned['variant_count'],
            difficulty_mix=cleaned['difficulty_mix'],
            format_mode=cleaned['format_mode'],
            extra_formats=extras,
            payload=payload,
        )
        generated.topics.set(cleaned['topics'])
    return generated


def kyrgyz_font_uris():
    regular = _DEJAVU
    bold = _DEJAVU_BOLD
    if not regular.is_file():
        fonts = Path(__file__).resolve().parent / 'generators' / 'fonts'
        regular = fonts / 'Inter-Regular.ttf'
        bold = fonts / 'Inter-Bold.ttf'
    return regular.resolve().as_uri(), bold.resolve().as_uri()


def render_test_pdf(payload):
    from weasyprint import HTML

    regular, bold = kyrgyz_font_uris()
    html = render_to_string('resources/test_maker_pdf.html', {
        'test': payload,
        'font_regular': regular,
        'font_bold': bold,
    })
    return HTML(string=html, base_url=str(settings.BASE_DIR)).write_pdf()


class TopicCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def __init__(self, attrs=None, choices=(), topic_stats=None):
        self.topic_stats = topic_stats or {}
        super().__init__(attrs, choices)

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs,
        )
        pk = getattr(value, 'value', value)
        try:
            pk = int(pk)
        except (TypeError, ValueError):
            pk = None
        counts = self.topic_stats.get(pk, {})
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
    topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.none(),
        label='Темалар',
        widget=forms.CheckboxSelectMultiple,
        error_messages={'required': 'Кеминде бир теманы белгилеңиз.'},
    )
    test_type = forms.ChoiceField(
        choices=GeneratedTest.TYPE_CHOICES,
        label='Тесттин түрү',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    question_count = forms.IntegerField(
        min_value=1,
        max_value=30,
        label='Суроолордун саны',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 30}),
        error_messages={
            'required': 'Суроолордун санын жазыңыз.',
            'invalid': 'Сан жазыңыз.',
            'min_value': 'Кеминде 1 суроо болушу керек.',
            'max_value': 'Эң көп 30 суроо.',
        },
    )
    difficulty_mix = forms.ChoiceField(
        choices=GeneratedTest.MIX_CHOICES,
        label='Деңгээл',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    format_mode = forms.ChoiceField(
        choices=FORMAT_MODE_CHOICES,
        label='Суроолордун түрү',
        widget=forms.RadioSelect,
        initial='mixed',
    )
    extra_formats = forms.MultipleChoiceField(
        choices=EXTRA_FORMAT_CHOICES,
        label='Кошумча түрлөр',
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    variant_count = forms.TypedChoiceField(
        coerce=int,
        choices=[(n, str(n)) for n in range(1, 5)],
        label='Варианттардын саны',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    def __init__(self, *args, topic_stats=None, **kwargs):
        self.topic_stats = topic_stats or {}
        super().__init__(*args, **kwargs)
        grades = available_grades(self.topic_stats)
        self.fields['grade'].choices = [(grade, f'{grade}-класс') for grade in grades]
        self.fields['topics'].queryset = Topic.objects.filter(
            pk__in=self.topic_stats,
        ).order_by('order', 'title')
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
            missing = [
                topic.title for topic in topics
                if grade not in self.topic_stats.get(topic.pk, {})
            ]
            if missing:
                self.add_error(
                    'topics',
                    'Бул класс үчүн тандалган темада суроо жок: ' + ', '.join(missing) + '.',
                )
        return cleaned


def initial_from_query(request, topic_stats):
    grades = available_grades(topic_stats)
    slugs = request.GET.getlist('tema')
    if not slugs and request.GET.get('tema'):
        slugs = [request.GET.get('tema')]
    topics = list(Topic.objects.filter(slug__in=slugs, pk__in=topic_stats))
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
            covered.update(topic_stats.get(topic.pk, {}))
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
        if grade in topic_stats.get(topic.pk, {})
    ]
    return {
        'grade': grade,
        'topics': topics,
        'test_type': GeneratedTest.TYPE_FORMATIVE,
        'question_count': 5,
        'difficulty_mix': GeneratedTest.MIX_EQUAL,
        'variant_count': 1,
        'format_mode': 'mixed',
        'extra_formats': [],
    }
