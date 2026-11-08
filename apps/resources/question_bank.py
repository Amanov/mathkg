"""Load the test-maker question bank built from the site's topic packs.

data/question_bank.json holds one entry per pack (grade 1 to 11). Its
questions come from the same sources as the pack files: the Жеңил, Орто
and Оор worksheet levels, the lesson deck (practice, worked examples,
«Ким туура?»), the hinge question, the exit ticket, the true/false maze,
the domino pairs, the bar-model problems and «Катаны тап». Every answer
was checked by the pack's own builder before the files were made.

Loading is idempotent: rows are matched by ``sample_key`` (``bank-…``),
new ones are added and existing ones are refreshed.
"""

import json
from pathlib import Path

BANK_FILE = Path(__file__).resolve().parent / 'data' / 'question_bank.json'
KEY_PREFIX = 'bank-'

AREA_TITLES = {
    'number': 'Сандар',
    'proportion': 'Пропорция',
    'algebra': 'Алгебра',
    'geometry': 'Геометрия',
    'probability': 'Ыктымалдуулук',
    'statistics': 'Дата',
}

FIELDS = (
    'grade', 'topic', 'theme', 'theme_slug', 'difficulty', 'question_format',
    'question_type', 'text', 'options', 'answer', 'solution', 'points',
    'estimated_minutes', 'is_published', 'is_sample',
)


def bank_themes():
    with open(BANK_FILE, encoding='utf-8') as fh:
        return json.load(fh)


def load_question_bank(Question, Topic):
    """Create or refresh every bank question. Returns (created, updated, skipped).

    Each pack hangs on its menu area («Сандар», «Геометрия»…). A pack whose
    area topic is not in the database yet is skipped; run the command again
    after the menu has been imported.
    """
    themes = bank_themes()
    areas = {
        topic.slug: topic
        for topic in Topic.objects.filter(slug__in={theme['area'] for theme in themes})
    }
    skipped = [theme['slug'] for theme in themes if theme['area'] not in areas]
    themes = [theme for theme in themes if theme['area'] in areas]

    existing = {
        row.sample_key: row
        for row in Question.objects.filter(sample_key__startswith=KEY_PREFIX)
    }
    new_rows, changed = [], []
    for theme in themes:
        for item in theme['questions']:
            values = {
                'grade': theme['grade'],
                'topic': areas[theme['area']],
                'theme': theme['title'],
                'theme_slug': theme['slug'],
                'difficulty': item['difficulty'],
                'question_format': item['question_format'],
                'question_type': item['question_type'],
                'text': item['text'],
                'options': item['options'],
                'answer': item['answer'],
                'solution': item['solution'],
                'points': item['points'],
                'estimated_minutes': item['estimated_minutes'],
                'is_published': True,
                'is_sample': False,
            }
            row = existing.get(item['sample_key'])
            if row is None:
                new_rows.append(Question(sample_key=item['sample_key'], **values))
                continue
            for field, value in values.items():
                setattr(row, field, value)
            changed.append(row)
    Question.objects.bulk_create(new_rows, batch_size=500)
    if changed:
        Question.objects.bulk_update(changed, [f for f in FIELDS if f != 'is_published'], batch_size=500)
    return len(new_rows), len(changed), len(skipped)
