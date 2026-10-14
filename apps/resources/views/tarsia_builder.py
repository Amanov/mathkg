import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from apps.resources.generators.tarsia_geom import edge_count
from apps.resources.generators.tarsia_pptx import build_tarsia_pptx
from apps.resources.generators.tarsia_svg import build_tarsia_svg

MIN_N = 3
MAX_N = 6


def tarsia_builder_view(request):
    sizes = [{'n': n, 'edges': edge_count(n), 'triangles': n * n} for n in range(MIN_N, MAX_N + 1)]
    return render(request, 'resources/tarsia_builder.html', {'sizes': sizes, 'default_n': 4})


def _parse_payload(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        return None, 'Туура эмес маалымат жөнөтүлдү.'

    try:
        n = int(data.get('n'))
    except (TypeError, ValueError):
        return None, 'Тор өлчөмү туура эмес.'
    if not MIN_N <= n <= MAX_N:
        return None, f'Тор өлчөмү {MIN_N}..{MAX_N} аралыгында болушу керек.'

    pairs = data.get('pairs')
    need = edge_count(n)
    if not isinstance(pairs, list) or len(pairs) != need:
        return None, f'{need} суроо-жооп жуптары керек, {len(pairs) if isinstance(pairs, list) else 0} берилди.'

    cleaned = []
    seen_answers = set()
    for item in pairs:
        if not isinstance(item, list) or len(item) != 2:
            return None, 'Жуптардын форматы туура эмес.'
        q, a = (str(item[0]).strip()[:60], str(item[1]).strip()[:60])
        if not q or not a:
            return None, 'Бардык суроо жана жооп талаалары толтурулушу керек.'
        if a in seen_answers:
            return None, f'Кайталанган жооп табылды: "{a}". Ар бир жооп уникалдуу болушу керек.'
        seen_answers.add(a)
        cleaned.append((q, a))

    title = str(data.get('title') or 'Тарсия').strip()[:120]
    usage_lines = data.get('usageLines') or []
    usage_lines = [str(line).strip()[:200] for line in usage_lines if str(line).strip()][:6]

    return {
        'n': n,
        'pairs': cleaned,
        'title': title,
        'usage_lines': usage_lines,
    }, None


@require_POST
def tarsia_builder_export_view(request):
    payload, error = _parse_payload(request)
    if error:
        return HttpResponseBadRequest(error)

    fmt = request.GET.get('format', 'pdf')
    base_name = ''.join(c for c in payload['title'] if c.isalnum()) or 'Tarsia'

    if fmt == 'pptx':
        buf = build_tarsia_pptx(
            payload['n'], payload['pairs'], payload['title'],
            payload['usage_lines'] or ['Үч бурчтуктарды кесип, жооптору дал келгендерин жанаштырыңыз.'],
            closing_email='mathematicskgz@gmail.com',
        )
        response = HttpResponse(
            buf.read(),
            content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation',
        )
        response['Content-Disposition'] = f'attachment; filename="{base_name}_Tarsia.pptx"'
        return response

    if fmt == 'pdf':
        from weasyprint import HTML  # Lazy import, see apps/resources/views/big4.py

        svg = build_tarsia_svg(payload['n'], payload['pairs'])
        html_string = render_to_string('interactive/tarsia_print.html', {
            'svg': svg,
            'title': payload['title'],
            'usage_lines': payload['usage_lines'],
        })
        pdf = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{base_name}_Tarsia.pdf"'
        return response

    return HttpResponseBadRequest('Белгисиз формат.')
