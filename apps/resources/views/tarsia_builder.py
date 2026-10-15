import json
import logging
import random

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from apps.resources.generators.loop_cards import build_loop_cards_pptx, build_loop_cards_svg, build_loop_order
from apps.resources.generators.tarsia_geom import edge_count
from apps.resources.generators.tarsia_pptx import build_tarsia_pptx
from apps.resources.generators.tarsia_svg import build_tarsia_svg

MIN_N = 3
MAX_N = 6
MIN_LOOP = 4
MAX_LOOP = 24

logger = logging.getLogger(__name__)


def tarsia_builder_view(request):
    sizes = [{'n': n, 'edges': edge_count(n), 'triangles': n * n} for n in range(MIN_N, MAX_N + 1)]
    return render(request, 'resources/tarsia_builder.html', {
        'sizes': sizes, 'default_n': 4, 'min_loop': MIN_LOOP, 'max_loop': MAX_LOOP,
    })


def _parse_payload(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        return None, 'Туура эмес маалымат жөнөтүлдү.'

    shape = data.get('shape') or 'triangle'
    if shape not in ('triangle', 'loop'):
        return None, 'Белгисиз форма.'

    if shape == 'triangle':
        try:
            n = int(data.get('n'))
        except (TypeError, ValueError):
            return None, 'Тор өлчөмү туура эмес.'
        if not MIN_N <= n <= MAX_N:
            return None, f'Тор өлчөмү {MIN_N}..{MAX_N} аралыгында болушу керек.'
        need = edge_count(n)
    else:
        n = None
        try:
            need = int(data.get('count'))
        except (TypeError, ValueError):
            return None, 'Карталардын саны туура эмес.'
        if not MIN_LOOP <= need <= MAX_LOOP:
            return None, f'Карталардын саны {MIN_LOOP}..{MAX_LOOP} аралыгында болушу керек.'

    pairs = data.get('pairs')
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
        'shape': shape,
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
    # ASCII-safe fallback: a pure-Cyrillic title leaves base_name empty after
    # encode/ignore, which previously produced a bare "_Tarsia.pptx" - fine,
    # but keep it explicit rather than relying on isalnum() alone.
    ascii_name = payload['title'].encode('ascii', 'ignore').decode('ascii')
    base_name = ''.join(c for c in ascii_name if c.isalnum()) or 'Tarsia'

    usage_lines = payload['usage_lines'] or ['Үч бурчтуктарды кесип, жооптору дал келгендерин жанаштырыңыз.']
    is_triangle = payload['shape'] == 'triangle'

    try:
        if is_triangle:
            # Shuffle which pair lands on which edge, so the printed/exported
            # sheet is NOT the pre-solved layout: cutting the triangles out
            # of a solved grid leaves matching values already adjacent,
            # which defeats the point of the cut-and-reassemble activity.
            shuffled_pairs = list(payload['pairs'])
            random.shuffle(shuffled_pairs)
        else:
            shuffled_pairs = payload['pairs']
            loop_order = build_loop_order(len(shuffled_pairs))

        if fmt == 'pptx':
            if is_triangle:
                buf = build_tarsia_pptx(
                    payload['n'], shuffled_pairs, payload['title'], usage_lines,
                    closing_email='mathematicskgz@gmail.com',
                )
            else:
                buf = build_loop_cards_pptx(
                    shuffled_pairs, payload['title'], usage_lines, order=loop_order,
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

            if is_triangle:
                svg = build_tarsia_svg(payload['n'], shuffled_pairs)
            else:
                svg = build_loop_cards_svg(shuffled_pairs, order=loop_order)
            html_string = render_to_string('interactive/tarsia_print.html', {
                'svg': svg,
                'title': payload['title'],
                'usage_lines': usage_lines,
            })
            pdf = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{base_name}_Tarsia.pdf"'
            return response
    except Exception:
        logger.exception('Tarsia export failed (format=%s, shape=%s, n=%s)', fmt, payload['shape'], payload['n'])
        return HttpResponseServerError(
            'Сервер жагынан ката кетти. Сураныч, кайра аракет кылыңыз же mathematicskgz@gmail.com дарегине жазыңыз.'
        )

    return HttpResponseBadRequest('Белгисиз формат.')
