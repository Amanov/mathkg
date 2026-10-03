"""Cards for /subtracting-1-digit/ (Кемитүү — 1 орундуу сандар).

The page does not look files up by Topic, Subtopic, or Subsubtopic.
``get_active_resources()`` loads every active Resource and this template
matches each file ``name`` to ``Resource.title`` exactly. A title that is
missing or inactive renders "Not found: <filename>". Thumbnails are the
static ``fallback_image`` files, used whenever the matched Resource has
no image of its own.

What makes a download button appear:
- Title equals the file name below, character for character.
- is_active is checked.
- A file is uploaded. The stored path can differ; the title is the key.

Category, learning goal, activity type, difficulty, and the topic
foreign keys are not read by this page. Leave the menu item's Topic /
Subtopic / Sub-subtopic blank too: those fields override url_name and
would send the menu link away from this page.
"""

# Section order shared with topic pages. A heading with no cards is
# left out, so Презентациялар, Көрсөтмө суроолор and Сынак суроолору
# are not rendered here.
SUBTRACTING_1_DIGIT_SECTIONS = [
    {
        "header": "Иш барактар",
        "blocks": [
            {
                "title": "Ылдам эсеп",
                "subtitle": "Кемитүү торчосу · 3 деңгээлде",
                "files": [
                    {"name": "kemituu-1orun-yldam-esep.pptx", "button": "PPT"},
                    {"name": "kemituu-1orun-yldam-esep.xlsx", "button": "EXC"},
                    {
                        "name": "kemituu-1orun-yldam-esep-A4.pdf",
                        "button": ".PDF",
                        "variant": "A4",
                    },
                ],
                "fallback_image": "img/kemituu-1orun-yldam-esep.png",
            },
            {
                "title": "Катаны тап",
                "files": [
                    {"name": "kemituu-1orun-katany-tap.pptx", "button": "PPT"},
                    {
                        "name": "kemituu-1orun-katany-tap-A4.pdf",
                        "button": ".PDF",
                        "variant": "A4",
                    },
                    {
                        "name": "kemituu-1orun-katany-tap-A5.pdf",
                        "button": ".PDF",
                        "variant": "A5",
                    },
                ],
                "fallback_image": "img/kemituu-1orun-katany-tap.png",
            },
            {
                "title": "Чоң санды түз",
                "subtitle": "Орун наркы боюнча жуп оюн",
                "files": [
                    {"name": "kemituu-1orun-chong-san.pptx", "button": "PPT"},
                    {
                        "name": "kemituu-1orun-chong-san-A5.pdf",
                        "button": ".PDF",
                        "variant": "A5",
                    },
                ],
                "fallback_image": "img/kemituu-1orun-chong-san.png",
            },
        ],
    },
    {
        "header": "Иш-чаралар",
        "blocks": [
            {
                "title": "Тарсия курак",
                "files": [
                    {"name": "kemituu-1orun-tarsia-kurak.pptx", "button": "PPT"},
                    {
                        "name": "kemituu-1orun-tarsia-kurak-standart.pdf",
                        "button": ".PDF",
                        "variant": "Стандарт",
                    },
                    {
                        "name": "kemituu-1orun-tarsia-kurak-kichine.pdf",
                        "button": ".PDF",
                        "variant": "Кичине",
                    },
                ],
                "fallback_image": "img/kemituu-1orun-tarsia-kurak.png",
            },
        ],
    },
    {
        "header": "Мугалим жетектеген иш-чаралар",
        "blocks": [
            {
                "title": "Бинго",
                "files": [
                    {"name": "kemituu-1orun-bingo.pptx", "button": "PPT"},
                ],
                "fallback_image": "img/kemituu-1orun-bingo.png",
            },
            {
                "title": "Катар үч",
                "subtitle": "Эки команда · 4 × 4 торчо",
                "files": [
                    {"name": "kemituu-1orun-katar-uch.pptx", "button": "PPT"},
                ],
                "fallback_image": "img/kemituu-1orun-katar-uch.png",
            },
        ],
    },
    {
        "header": "Көрсөтмө куралдар",
        "blocks": [
            {
                "title": "Ондук чарчылар",
                "subtitle": "Бирдик · ондон бир · жүздөн бир",
                "files": [
                    {"name": "kemituu-1orun-onduk-charchylar.pptx", "button": "PPT"},
                    {
                        "name": "kemituu-1orun-onduk-charchylar-tustuu.pdf",
                        "button": ".PDF",
                        "variant": "Түстүү",
                    },
                    {
                        "name": "kemituu-1orun-onduk-charchylar-ak-kara.pdf",
                        "button": ".PDF",
                        "variant": "Ак-кара",
                    },
                ],
                "fallback_image": "img/kemituu-1orun-onduk-charchylar.png",
            },
            {
                "title": "Орун наркы таблицасы",
                "files": [
                    {"name": "kemituu-1orun-orun-narky-tablitsasy.pptx", "button": "PPT"},
                    {
                        "name": "kemituu-1orun-orun-narky-tablitsasy-chong.pdf",
                        "button": ".PDF",
                        "variant": "Чоң",
                    },
                    {
                        "name": "kemituu-1orun-orun-narky-tablitsasy-standart.pdf",
                        "button": ".PDF",
                        "variant": "Стандарт",
                    },
                    {
                        "name": "kemituu-1orun-orun-narky-tablitsasy-kichine.pdf",
                        "button": ".PDF",
                        "variant": "Кичине",
                    },
                ],
                "fallback_image": "img/kemituu-1orun-orun-narky-tablitsasy.png",
            },
        ],
    },
]
