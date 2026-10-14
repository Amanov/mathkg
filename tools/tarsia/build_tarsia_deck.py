#!/usr/bin/env python3
"""Build a full Tarsia activity: title/instructions + full-bleed puzzle
slide (PPTX, matching the reference decks' structure) plus a standalone
print-ready PDF. No branding/watermarks are added - this only draws the
triangle grid and whatever text you pass it.

Usage (see SKILL.md for the full walkthrough):

    from build_tarsia_deck import build_tarsia_activity
    build_tarsia_activity(
        n=4,
        pairs=[("0.3 + 0.4", "0.7"), ...],   # must be geom.edge_count(n) long
        title="Ондуктарды кошуу - Тарсия",
        usage_lines=["Кесип, жооптору дал келгендерин жанаштырыңыз."],
        out_dir="/path/to/out",
        base_name="OnduktarduKoshuuTarsia",
    )
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from tarsia import render_tarsia
from geom import edge_count

INK = '1F2A44'
MUTED = '5B6472'
WHITE = 'FFFFFF'
AMBER = 'F2A33F'


def build_tarsia_activity(n, pairs, title, usage_lines, out_dir, base_name,
                           closing_lines=('Суроолор барбы?', 'Сунуштар?'),
                           closing_email=None):
    """Writes {base_name}.pptx and {base_name}.pdf into out_dir. Also leaves
    {base_name}_puzzle.png (the rendered puzzle alone, for re-use)."""
    os.makedirs(out_dir, exist_ok=True)
    need = edge_count(n)
    if len(pairs) != need:
        raise ValueError(f'n={n} needs exactly {need} pairs, got {len(pairs)}')

    png_path = os.path.join(out_dir, f'{base_name}_puzzle.png')
    pdf_path = os.path.join(out_dir, f'{base_name}.pdf')
    render_tarsia(n, pairs, out_png=png_path, out_pdf=pdf_path)

    pptx_path = os.path.join(out_dir, f'{base_name}.pptx')
    _write_pptx_via_node(png_path, pptx_path, title, usage_lines, closing_lines, closing_email)
    return {'pptx': pptx_path, 'pdf': pdf_path, 'png': png_path}


def _write_pptx_via_node(png_path, pptx_path, title, usage_lines, closing_lines, closing_email):
    """Shells out to Node + pptxgenjs (same stack already used project-wide
    for slide generation) to assemble the deck. Requires pptxgenjs to be
    resolvable from NODE_PATH or a local node_modules."""
    import json
    import subprocess
    import tempfile

    script = r'''
const pptxgen = require(process.env.TARSIA_PPTXGENJS);
const [, , cfgPath] = process.argv;
const cfg = JSON.parse(require('fs').readFileSync(cfgPath, 'utf8'));

const INK = '1F2A44', MUTED = '5B6472', WHITE = 'FFFFFF', AMBER = 'F2A33F';

const p = new pptxgen();
p.layout = 'LAYOUT_WIDE';

{
  const s = p.addSlide();
  s.addText(cfg.title, { x: 0.6, y: 0.5, w: 12.1, h: 1.1, fontSize: 28, bold: true, color: INK, fontFace: 'Calibri', isTextBox: true });
  const paras = cfg.usageLines.map((t, i) => ({ text: t, options: { breakLine: i < cfg.usageLines.length - 1, color: MUTED } }));
  s.addText(paras, { x: 0.6, y: 1.8, w: 12.1, h: 3, fontSize: 15, fontFace: 'Calibri', isTextBox: true, paraSpaceAfter: 10, lineSpacingMultiple: 1.2 });
}
{
  const s = p.addSlide();
  s.addImage({ path: cfg.pngPath, x: 1.4, y: 0.3, w: 10.5, h: 6.9, sizing: { type: 'contain', w: 10.5, h: 6.9 } });
}
{
  const s = p.addSlide();
  s.background = { color: INK };
  s.addText(cfg.closingLines.join('\n'), { x: 0.8, y: 2.0, w: 11.7, h: 1.6, fontSize: 30, bold: true, color: WHITE, fontFace: 'Calibri', isTextBox: true });
  if (cfg.closingEmail) {
    s.addText(cfg.closingEmail, { x: 0.8, y: 3.8, w: 11.7, h: 0.6, fontSize: 14, color: 'C7D2E8', fontFace: 'Calibri', isTextBox: true });
  }
}
p.writeFile({ fileName: cfg.pptxPath }).then(() => console.log('ok'));
'''
    pptxgenjs_path = os.environ.get('TARSIA_PPTXGENJS')
    if not pptxgenjs_path:
        for candidate in (
            os.path.join(os.path.dirname(__file__), 'node_modules', 'pptxgenjs'),
        ):
            if os.path.exists(candidate):
                pptxgenjs_path = candidate
                break
    if not pptxgenjs_path:
        raise RuntimeError(
            'Set TARSIA_PPTXGENJS to the pptxgenjs module path (e.g. a scratchpad '
            'node_modules/pptxgenjs install) before calling build_tarsia_activity.'
        )

    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as sf:
        sf.write(script)
        script_path = sf.name
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as cf:
        json.dump({
            'title': title,
            'usageLines': list(usage_lines),
            'pngPath': png_path,
            'pptxPath': pptx_path,
            'closingLines': list(closing_lines),
            'closingEmail': closing_email,
        }, cf)
        cfg_path = cf.name

    env = dict(os.environ)
    env['TARSIA_PPTXGENJS'] = pptxgenjs_path
    result = subprocess.run(['node', script_path, cfg_path], capture_output=True, text=True, env=env)
    if result.returncode != 0:
        raise RuntimeError(f'pptx generation failed: {result.stderr}')
