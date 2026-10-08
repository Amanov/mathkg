from django.http import Http404
from django.shortcuts import render

from apps.resources.lesson_flow import (
    BLOOM_LEVELS,
    STAGE_BY_SLUG,
    STAGES,
    all_materials,
    stages_with_counts,
)
from apps.resources.models import MenuItem, NewsPost


def home_screen_view(request):
    materials = all_materials()
    stages = stages_with_counts(materials)

    # Which stages work on each Bloom level - the ladder on the landing
    # page reads it the other way round from STAGES.
    bloom_ladder = []
    for level in reversed(BLOOM_LEVELS):
        bloom_ladder.append({
            **level,
            'stages': [s for s in stages if level['key'] in s['bloom']],
        })

    return render(request, 'resources/landing.html', {
        'materials': materials,
        'stages_5e': [s for s in stages if s['group'] == '5e'],
        'stages_3c': [s for s in stages if s['group'] == '3c'],
        'bloom_ladder': bloom_ladder,
        'material_count': len(materials),
        'page_count': len({m['url'] for m in materials}),
        'topic_count': MenuItem.objects.count(),
        'latest_news': NewsPost.objects.all()[:3],
    })


def lesson_stage_view(request, stage_slug):
    stage = STAGE_BY_SLUG.get(stage_slug)
    if stage is None:
        raise Http404
    materials = all_materials()
    stages = stages_with_counts(materials)
    current = next(s for s in stages if s['slug'] == stage_slug)
    index = [s['slug'] for s in STAGES].index(stage_slug)

    return render(request, 'resources/lesson_stage.html', {
        'stage': current,
        'stages': stages,
        'materials': [m for m in materials if m['stage']['slug'] == stage_slug],
        'prev_stage': stages[index - 1] if index > 0 else None,
        'next_stage': stages[index + 1] if index + 1 < len(stages) else None,
    })


def success_view(request):

    return render(
        request,
        'resources/sandar/SuccessMessage.html',
        {}
    )
