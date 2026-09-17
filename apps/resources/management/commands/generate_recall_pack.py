import os

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from apps.resources.generators.geometry_svg import build_reflection_svg
from apps.resources.generators.grid_layout import cell_rect_pct
from apps.resources.generators.pptx_builder import build_presentation
from apps.resources.generators.recall_pack import generate_pack


def _attach_layout_and_svg(pack):
    for q in pack["questions"]:
        left, top, width, height = cell_rect_pct(q["number"])
        q["rect"] = {"left": left, "top": top, "width": width, "height": height}
        if "svg_points" in q:
            q["svg"] = True
            q["svg_html_blank"] = mark_safe(build_reflection_svg(
                q["svg_points"], q["svg_reflected"], q["svg_mirror_x"], show_answer=False,
            ))
            q["svg_html_answer"] = mark_safe(build_reflection_svg(
                q["svg_points"], q["svg_reflected"], q["svg_mirror_x"], show_answer=True,
            ))


def _render_pdf(pack, page_size):
    from weasyprint import HTML

    sizing = {
        "A4": {"page_margin": "12mm", "grid_height": "245mm", "base_font_size": "10.5pt"},
        "A5": {"page_margin": "8mm", "grid_height": "165mm", "base_font_size": "7.6pt"},
    }[page_size]
    html_string = render_to_string("interactive/recall_pack_print.html", {
        "pack": pack,
        "pages": [False, True],
        "page_size": page_size,
        **sizing,
    })
    return HTML(string=html_string).write_pdf()


class Command(BaseCommand):
    help = "Generates a Kyrgyz recall/retrieval-practice worksheet pack (A4 PDF, A5 PDF, PPTX)."

    def add_arguments(self, parser):
        parser.add_argument("--seed", type=int, default=None, help="Random seed (omit for a fresh random pack).")
        parser.add_argument("--pack-code", type=str, default="1-А", help='Pack label, e.g. "1-А", "1-Б".')
        parser.add_argument("--slug", type=str, default="toptom-1-a", help="Filename-safe slug for the output files.")
        parser.add_argument("--out-dir", type=str, default="media/resources/files/kyrgyz_recall", help="Output directory.")

    def handle(self, *args, **options):
        seed = options["seed"]
        pack_code = options["pack_code"]
        slug = options["slug"]
        out_dir = options["out_dir"]

        pack = generate_pack(seed=seed, pack_code=pack_code)
        _attach_layout_and_svg(pack)

        os.makedirs(out_dir, exist_ok=True)

        a4_path = os.path.join(out_dir, f"{slug}-A4.pdf")
        with open(a4_path, "wb") as f:
            f.write(_render_pdf(pack, "A4"))
        self.stdout.write(self.style.SUCCESS(f"Written {a4_path}"))

        a5_path = os.path.join(out_dir, f"{slug}-A5.pdf")
        with open(a5_path, "wb") as f:
            f.write(_render_pdf(pack, "A5"))
        self.stdout.write(self.style.SUCCESS(f"Written {a5_path}"))

        pptx_path = os.path.join(out_dir, f"{slug}.pptx")
        build_presentation(pack).save(pptx_path)
        self.stdout.write(self.style.SUCCESS(f"Written {pptx_path}"))

        self.stdout.write(f"Total marks: {pack['total_marks']}")
