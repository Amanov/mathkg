from datetime import datetime
import random

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string


# ====================== HELPER FUNCTIONS ======================
def number_to_words(num):
    """Convert number to words (used in questions)"""
    if num == 0:
        return "zero"
    ones = [
        "",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
        "eleven",
        "twelve",
        "thirteen",
        "fourteen",
        "fifteen",
        "sixteen",
        "seventeen",
        "eighteen",
        "nineteen",
    ]
    tens = [
        "",
        "",
        "twenty",
        "thirty",
        "forty",
        "fifty",
        "sixty",
        "seventy",
        "eighty",
        "ninety",
    ]

    words = ""
    n = abs(round(num))
    if n >= 1000:
        words += ones[n // 1000] + " thousand"
        n %= 1000
        if n > 0:
            words += " "
    if n >= 100:
        words += ones[n // 100] + " hundred"
        n %= 100
        if n > 0:
            words += " and "
    if n >= 20:
        words += tens[n // 10]
        if n % 10 > 0:
            words += "-" + ones[n % 10]
    elif n > 0:
        words += ones[n]
    return words.strip()


def create_challenge_data(level, difficulty):
    """Ported logic from JavaScript"""
    if level == "7":
        if difficulty == 1:
            target = random.randint(10, 99)
            addsub = random.randint(1, 20)
            prop_q = "Is the number Even or Odd?"
            prop_a = "Even" if target % 2 == 0 else "Odd"
            mult = random.choice([2, 10])
        elif difficulty == 2:
            target = random.randint(100, 999)
            addsub = random.randint(10, 50)
            prop_q = "Round to the nearest 10"
            prop_a = round(target / 10) * 10
            mult = random.choice([5, 20])
        else:
            target = random.randint(1000, 9999)
            addsub = random.randint(50, 250)
            prop_q = "Round to the nearest 100"
            prop_a = round(target / 100) * 100
            mult = random.choice([50, 100])

        is_add = random.random() > 0.5
        q1_text = f"Add {addsub}" if is_add else f"Subtract {addsub}"
        q1_ans = target + addsub if is_add else target - addsub

        return {
            "target": target,
            "questions": [
                {"id": 1, "text": q1_text, "answer": q1_ans},
                {
                    "id": 2,
                    "text": "Write the number in words",
                    "answer": number_to_words(target),
                },
                {"id": 3, "text": prop_q, "answer": prop_a},
                {
                    "id": 4,
                    "text": f"Multiply the number by {mult}",
                    "answer": target * mult,
                },
            ],
        }

    elif level == "8":
        target = random.randint(100, 9999)
        return {
            "target": target,
            "questions": [
                {
                    "id": 1,
                    "text": f"Add {random.randint(50, 300)}",
                    "answer": target + 150,
                },
                {
                    "id": 2,
                    "text": "Find 25% of the number",
                    "answer": target // 4,
                },
                {
                    "id": 3,
                    "text": "Divide the number by 10",
                    "answer": target // 10,
                },
                {
                    "id": 4,
                    "text": "Write the number in words",
                    "answer": number_to_words(target),
                },
            ],
        }
    else:  # Year 9
        target = round(random.uniform(10.0, 89.9), 2)
        return {
            "target": target,
            "questions": [
                {"id": 1, "text": "Add 4.5", "answer": round(target + 4.5, 2)},
                {
                    "id": 2,
                    "text": "Multiply by 0.2",
                    "answer": round(target * 0.2, 3),
                },
                {
                    "id": 3,
                    "text": "Round to 2 decimal places",
                    "answer": round(target, 2),
                },
                {
                    "id": 4,
                    "text": "Increase by 15%",
                    "answer": round(target * 1.15, 2),
                },
            ],
        }


# ====================== MAIN VIEW ======================
def big4_view(request):
    # PDF Download
    if request.GET.get("pdf") == "1":
        from weasyprint import HTML  # Lazy import inside the view

        level = request.GET.get("level", "7")
        count = int(request.GET.get("count", 1))
        progressive = request.GET.get("progressive") == "1"
        difficulty = int(request.GET.get("difficulty", 1))

        sheets = []
        curr_diff = difficulty
        for i in range(count):
            if progressive and i > 0:
                curr_diff = (curr_diff % 3) + 1
            sheets.append(create_challenge_data(level, curr_diff))

        context = {
            "level": level,
            "sheets": sheets,
            "today": datetime.now().strftime("%d %B %Y"),
        }

        html_string = render_to_string("interactive/big4_print.html", context)
        pdf = HTML(
            string=html_string, base_url=request.build_absolute_uri("/")
        ).write_pdf()

        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="Big4_Worksheet_Year{level}.pdf"'
        )
        return response

    # Normal page render
    return render(request, "interactive/big4.html", {})