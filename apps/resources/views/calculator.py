from apps.resources.views.onduktar_placeholders import pack_or_placeholder

# Сандар > Калькулятор колдонуу > Калькулятордо бөлчөктөр. Its old files
# were built on goteachmaths templates and were taken off the site
# (2026-10-24, migration 0033). Since 2026-11-08 the page shows the grade 8
# approximation and calculator pack (data/pack_pages.py). The
# CALCULATOR_FRACTIONS spec is kept for reference only.


def calculator_fractions_view(request):
    return pack_or_placeholder(request, 'calculator-fractions', 'Калькулятордо бөлчөктөр')
