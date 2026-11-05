/* Reusable onboarding tooltip. Steps are {selector, title, body}. */
(function () {
    var TOURS = {
        welcome: [
            {
                title: 'Кош келиңиз',
                body: 'MathKG — мугалимдер үчүн математикалык материалдар. Кыскача көрсөтөбүз.'
            },
            {
                selector: '[data-tour="search"]',
                title: 'Издөө',
                body: 'Класс боюнча издөө. Мисалы, «5-класс» деп жазыңыз.'
            },
            {
                selector: '[data-tour="topics"]',
                title: 'Темалар',
                body: 'Менюдан темаларды жана материалдарды ачыңыз.'
            },
            {
                selector: '[data-tour="test-button"]',
                title: 'Тест түзүү',
                body: 'Ушул баскыч менен өз тестиңизди түзөсүз.'
            },
            {
                selector: '[data-tour="account"]',
                title: 'Аккаунт',
                body: 'Профилиңиз жана жазылууңуз ушул жерде.'
            },
            {
                selector: '[data-tour="feedback"]',
                title: 'Пикир',
                body: 'Барактын астындагы жүздөр менен баа калтырыңыз.'
            }
        ],
        test: [
            {
                selector: '[data-tour="class-topics"]',
                title: 'Класс жана тема',
                body: 'Адегенде классты жана темаларды тандаңыз.'
            },
            {
                selector: '[data-tour="test-name"]',
                title: 'Тесттин аты',
                body: 'Кааласаңыз, тестке ат коюңуз. Ал PDF барагында көрүнөт.'
            },
            {
                selector: '[data-tour="formats"]',
                title: 'Суроолордун түрү',
                body: 'Кеминде бир түрдү белгилеңиз. Тандалганда белги чыгат.'
            },
            {
                selector: '[data-tour="levels"]',
                title: 'Деңгээл',
                body: 'Жеңил, орто, оор же өтө оор деңгээлди тандаңыз.'
            },
            {
                selector: '[data-tour="time"]',
                title: 'Убакыт',
                body: 'Узактыкты сыдырма менен коюңуз. Кааласаңыз, убакыт PDF барагында көрүнөт.'
            },
            {
                selector: '[data-tour="pdf"]',
                title: 'PDF түзүү',
                body: 'Даяр болгондо PDF файлын жүктөп алыңыз.'
            }
        ]
    };

    var state = null;
    var tip = null;
    var highlighted = null;

    function csrf() {
        var node = document.querySelector('meta[name="csrf-token"]');
        return node ? node.getAttribute('content') : '';
    }

    function markSeen(name) {
        var url = document.body.getAttribute('data-tour-url');
        if (!url) return;
        var body = new FormData();
        body.append('tour', name === 'test' ? 'test' : 'welcome');
        fetch(url, {
            method: 'POST',
            headers: {'X-CSRFToken': csrf()},
            body: body,
            credentials: 'same-origin'
        }).catch(function () {});
    }

    function ensureTip() {
        if (tip) return tip;
        tip = document.createElement('div');
        tip.className = 'tour-tip';
        tip.setAttribute('role', 'dialog');
        tip.setAttribute('aria-modal', 'false');
        tip.innerHTML = ''
            + '<button type="button" class="tour-tip__close" aria-label="Жабуу">✕</button>'
            + '<p class="tour-tip__title"></p>'
            + '<p class="tour-tip__body"></p>'
            + '<div class="tour-tip__row">'
            + '  <span class="tour-tip__count"></span>'
            + '  <span class="tour-tip__actions">'
            + '    <button type="button" class="tour-tip__back">Артка</button>'
            + '    <button type="button" class="tour-tip__next">Кийинки</button>'
            + '  </span>'
            + '</div>';
        document.body.appendChild(tip);
        tip.querySelector('.tour-tip__close').addEventListener('click', function () { finish(true); });
        tip.querySelector('.tour-tip__back').addEventListener('click', function () { move(-1); });
        tip.querySelector('.tour-tip__next').addEventListener('click', function () { move(1); });
        window.addEventListener('resize', place);
        window.addEventListener('scroll', place, true);
        return tip;
    }

    function reveal(el) {
        if (!el) return;
        if (window.matchMedia('(max-width: 991px)').matches) {
            var collapse = el.closest('.site-nav-collapse');
            if (collapse) collapse.classList.add('show');
        }
        try {
            el.scrollIntoView({block: 'center', inline: 'nearest'});
        } catch (e) {
            el.scrollIntoView();
        }
    }

    function clearHighlight() {
        if (highlighted) {
            highlighted.classList.remove('tour-target');
            highlighted = null;
        }
    }

    function place() {
        if (!state || !tip) return;
        var step = state.steps[state.index];
        var el = step.selector ? document.querySelector(step.selector) : null;
        clearHighlight();
        if (el) {
            reveal(el);
            el.classList.add('tour-target');
            highlighted = el;
        }
        tip.hidden = false;
        var margin = 12;
        var width = Math.min(320, window.innerWidth - margin * 2);
        tip.style.width = width + 'px';
        var rect = tip.getBoundingClientRect();
        var top;
        var left;
        if (!el) {
            tip.dataset.place = 'center';
            top = Math.max(margin, (window.innerHeight - rect.height) / 2);
            left = Math.max(margin, (window.innerWidth - width) / 2);
        } else {
            var target = el.getBoundingClientRect();
            var below = target.bottom + 16;
            var placeBelow = below + rect.height <= window.innerHeight - margin;
            if (placeBelow) {
                tip.dataset.place = 'bottom';
                top = below;
            } else {
                tip.dataset.place = 'top';
                top = Math.max(margin, target.top - rect.height - 16);
            }
            left = target.left + target.width / 2 - width / 2;
            left = Math.max(margin, Math.min(left, window.innerWidth - width - margin));
            var arrow = target.left + target.width / 2 - left;
            arrow = Math.max(18, Math.min(arrow, width - 18));
            tip.style.setProperty('--arrow-x', arrow + 'px');
        }
        if (top + rect.height > window.innerHeight - margin) {
            top = Math.max(margin, window.innerHeight - rect.height - margin);
        }
        tip.style.top = top + 'px';
        tip.style.left = left + 'px';
    }

    function show() {
        var node = ensureTip();
        var step = state.steps[state.index];
        node.querySelector('.tour-tip__title').textContent = step.title;
        node.querySelector('.tour-tip__body').textContent = step.body;
        node.querySelector('.tour-tip__count').textContent = (state.index + 1) + ' / ' + state.steps.length;
        var back = node.querySelector('.tour-tip__back');
        back.hidden = state.index === 0;
        node.querySelector('.tour-tip__next').textContent = state.index === state.steps.length - 1 ? 'Бүттү' : 'Кийинки';
        place();
    }

    function move(delta) {
        if (!state) return;
        var next = state.index + delta;
        if (next < 0) return;
        if (next >= state.steps.length) {
            finish(true);
            return;
        }
        state.index = next;
        show();
    }

    function finish(seen) {
        if (!state) return;
        var done = state.onDone;
        var name = state.name;
        var replay = state.replay;
        clearHighlight();
        if (tip) tip.hidden = true;
        state = null;
        if (seen && !replay) markSeen(name);
        if (done) done();
    }

    function start(name, options) {
        options = options || {};
        if (!TOURS[name]) return;
        if (state) finish(false);
        state = {
            name: name,
            steps: TOURS[name],
            index: 0,
            onDone: options.onDone || null,
            replay: !!options.replay
        };
        show();
    }

    document.addEventListener('click', function (event) {
        var button = event.target.closest('[data-tour-replay]');
        if (!button) return;
        event.preventDefault();
        start(button.getAttribute('data-tour-replay'), {replay: true});
    });

    document.addEventListener('DOMContentLoaded', function () {
        var welcome = document.body.getAttribute('data-welcome-tour') === '1';
        var test = document.body.getAttribute('data-test-tour') === '1';
        function startTest() {
            if (document.querySelector('[data-tour="class-topics"]')) start('test');
        }
        if (welcome) start('welcome', {onDone: test ? startTest : null});
        else if (test) startTest();
    });

    window.MathKGTour = {start: start};
})();
