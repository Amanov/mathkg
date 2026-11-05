"""Sample grade 5–6 questions for the test maker.

Pure Kyrgyz. Decimals use a comma. Thousands use a space. Word problems
say «маселени чыгар» and «окуучу». Each answer is checked in
apps/resources/test_assessment.py.

The seed prefers an existing topic titled «Бөлчөктөр» or «Ондуктар».
If that row is missing, it creates a topic marked «(үлгү)».
"""

NBSP = '\u00a0'

FALLBACK_TOPIC_SLUGS = ('ulgu-bolchoktor', 'ulgu-onduktar')

TOPIC_SPECS = (
    {
        'key': 'bolchok',
        'match_title': 'Бөлчөктөр',
        'fallback_slug': 'ulgu-bolchoktor',
        'fallback_title': 'Бөлчөктөр (үлгү)',
    },
    {
        'key': 'onduk',
        'match_title': 'Ондуктар',
        'fallback_slug': 'ulgu-onduktar',
        'fallback_title': 'Ондуктар (үлгү)',
    },
)

SAMPLE_QUESTIONS = (
    {
        'sample_key': 'ulgu-f-half-quarter',
        'topic_key': 'bolchok',
        'grade': 5,
        'difficulty': 'easy',
        'question_type': 'multiple_choice',
        'text': '1/2 + 1/4 канчага барабар?',
        'options': {'А': '1/4', 'Б': '3/4', 'В': '2/6', 'Г': '2/4'},
        'answer': 'Б',
        'points': 1,
    },
    {
        'sample_key': 'ulgu-f-same-den',
        'topic_key': 'bolchok',
        'grade': 5,
        'difficulty': 'easy',
        'question_type': 'short_answer',
        'text': '2/7 + 3/7 канчага барабар?',
        'options': {},
        'answer': '5/7',
        'points': 1,
    },
    {
        'sample_key': 'ulgu-f-of-whole',
        'topic_key': 'bolchok',
        'grade': 5,
        'difficulty': 'medium',
        'question_type': 'multiple_choice',
        'text': '20 санынын 3/5 бөлүгү канча?',
        'options': {'А': '10', 'Б': '12', 'В': '15', 'Г': '8'},
        'answer': 'Б',
        'points': 2,
    },
    {
        'sample_key': 'ulgu-f-subtract',
        'topic_key': 'bolchok',
        'grade': 5,
        'difficulty': 'hard',
        'question_type': 'short_answer',
        'text': '5/6 − 1/2 канчага барабар? Жоопту жөнөкөй түрүндө жаз.',
        'options': {},
        'answer': '1/3',
        'points': 3,
    },
    {
        'sample_key': 'ulgu-f-cloth',
        'topic_key': 'bolchok',
        'grade': 5,
        'difficulty': 'medium',
        'question_type': 'word_problem',
        'text': (
            f'Маселени чыгар. {1}{NBSP}000 м кездеменин 1/4 бөлүгү кесилди. '
            'Канча метр калды?'
        ),
        'options': {},
        'answer': '750',
        'points': 2,
    },
    {
        'sample_key': 'ulgu-f-divide',
        'topic_key': 'bolchok',
        'grade': 6,
        'difficulty': 'hard',
        'question_type': 'multiple_choice',
        'text': '2/3 : 1/6 канчага барабар?',
        'options': {'А': '1/9', 'Б': '4', 'В': '1/4', 'Г': '3'},
        'answer': 'Б',
        'points': 3,
    },
    {
        'sample_key': 'ulgu-f-equal',
        'topic_key': 'bolchok',
        'grade': 6,
        'difficulty': 'medium',
        'question_type': 'multiple_choice',
        'text': '1/2, 0,5 жана 3/6 салыштыр. Кайсысы туура?',
        'options': {
            'А': '1/2 башкаларынан чоң',
            'Б': '0,5 башкаларынан кичине',
            'В': 'үчөө тең барабар',
            'Г': '3/6 башкаларынан чоң',
        },
        'answer': 'В',
        'points': 2,
    },
    {
        'sample_key': 'ulgu-d-add',
        'topic_key': 'onduk',
        'grade': 5,
        'difficulty': 'easy',
        'question_type': 'multiple_choice',
        'text': '0,3 + 0,4 канчага барабар?',
        'options': {'А': '0,7', 'Б': '0,34', 'В': '0,07', 'Г': '7'},
        'answer': 'А',
        'points': 1,
    },
    {
        'sample_key': 'ulgu-d-mul',
        'topic_key': 'onduk',
        'grade': 5,
        'difficulty': 'medium',
        'question_type': 'short_answer',
        'text': '2,5 × 4 канчага барабар?',
        'options': {},
        'answer': '10',
        'points': 2,
    },
    {
        'sample_key': 'ulgu-d-apples',
        'topic_key': 'onduk',
        'grade': 5,
        'difficulty': 'medium',
        'question_type': 'word_problem',
        'text': (
            'Маселени чыгар. 1 кг алма 80 сом. Окуучу 2,5 кг алма сатып алды. '
            'Канча сом төлөйт?'
        ),
        'options': {},
        'answer': '200',
        'points': 3,
    },
    {
        'sample_key': 'ulgu-d-to-fraction',
        'topic_key': 'onduk',
        'grade': 6,
        'difficulty': 'medium',
        'question_type': 'short_answer',
        'text': '0,75ти жөнөкөй бөлчөккө айландырып жаз.',
        'options': {},
        'answer': '3/4',
        'points': 2,
    },
    {
        'sample_key': 'ulgu-d-area',
        'topic_key': 'onduk',
        'grade': 6,
        'difficulty': 'hard',
        'question_type': 'word_problem',
        'text': (
            'Маселени чыгар. Тик бурчтуктун узундугу 3,5 м, кеңдиги 2 м. '
            'Аянты канча квадрат метр?'
        ),
        'options': {},
        'answer': '7',
        'points': 3,
    },
)


def _topic_for(Topic, spec):
    real = (
        Topic.objects.filter(title__iexact=spec['match_title'])
        .exclude(slug=spec['fallback_slug'])
        .order_by('pk')
        .first()
    )
    if real is not None:
        return real, False
    topic, created = Topic.objects.get_or_create(
        slug=spec['fallback_slug'],
        defaults={'title': spec['fallback_title'], 'order': 900},
    )
    if topic.title != spec['fallback_title']:
        topic.title = spec['fallback_title']
        topic.save(update_fields=['title'])
    return topic, created


def seed_sample_questions(Question, Topic):
    """Insert or refresh the sample bank. Safe to run more than once."""
    topics = {}
    topics_created = 0
    for spec in TOPIC_SPECS:
        topic, created = _topic_for(Topic, spec)
        topics[spec['key']] = topic
        topics_created += int(created)

    created_q = 0
    updated_q = 0
    for row in SAMPLE_QUESTIONS:
        defaults = {
            'topic': topics[row['topic_key']],
            'grade': row['grade'],
            'difficulty': row['difficulty'],
            'question_type': row['question_type'],
            'text': row['text'],
            'options': row['options'],
            'answer': row['answer'],
            'points': row['points'],
            'is_sample': True,
            'is_published': True,
        }
        _, was_created = Question.objects.update_or_create(
            sample_key=row['sample_key'],
            defaults=defaults,
        )
        if was_created:
            created_q += 1
        else:
            updated_q += 1
    return {
        'topics_created': topics_created,
        'created': created_q,
        'updated': updated_q,
    }
