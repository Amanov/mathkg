from apps.resources.views.onduktar_placeholders import placeholder_page

# Сандар > Калькулятор колдонуу > Калькулятордо бөлчөктөр. Its four files
# were built on goteachmaths templates and were taken off the site
# (2026-10-24, migration 0033), so the page shows the «даярдалууда»
# placeholder. The CALCULATOR_FRACTIONS spec is kept for reference only.


def calculator_fractions_view(request):
    return placeholder_page(request, 'Калькулятордо бөлчөктөр')
