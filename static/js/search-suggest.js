document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('siteSearchInput');
    const panel = document.getElementById('siteSearchSuggest');
    if (!input || !panel) return;

    const form = input.closest('form');
    const MIN_CHARS = 2;
    const DEBOUNCE_MS = 200;

    let debounceTimer = null;
    let activeController = null;
    let activeIndex = -1;

    function closePanel() {
        panel.hidden = true;
        panel.innerHTML = '';
        activeIndex = -1;
        input.setAttribute('aria-expanded', 'false');
    }

    function items() {
        return Array.from(panel.querySelectorAll('.search-suggest-item'));
    }

    function setActive(index) {
        const list = items();
        if (!list.length) return;
        list.forEach(el => el.classList.remove('is-active'));
        activeIndex = (index + list.length) % list.length;
        const el = list[activeIndex];
        el.classList.add('is-active');
        el.scrollIntoView({ block: 'nearest' });
    }

    function renderResults(query, results) {
        panel.innerHTML = '';

        if (!results.length) {
            const empty = document.createElement('div');
            empty.className = 'search-suggest-empty';
            empty.textContent = 'Эч нерсе табылган жок';
            panel.appendChild(empty);
        } else {
            results.forEach(function (result) {
                const link = document.createElement('a');
                link.className = 'search-suggest-item';
                link.setAttribute('role', 'option');
                link.href = result.url;

                if (result.breadcrumb && result.breadcrumb.length) {
                    const crumb = document.createElement('span');
                    crumb.className = 'search-suggest-breadcrumb';
                    crumb.textContent = result.breadcrumb.join(' › ');
                    link.appendChild(crumb);
                }

                const title = document.createElement('span');
                title.className = 'search-suggest-title';
                title.textContent = result.title;
                link.appendChild(title);

                panel.appendChild(link);
            });
        }

        const footer = document.createElement('a');
        footer.className = 'search-suggest-footer';
        footer.href = form.action + '?q=' + encodeURIComponent(query);
        footer.textContent = 'Толук жыйынтыктарды көрсөт';
        panel.appendChild(footer);

        panel.hidden = false;
        activeIndex = -1;
        input.setAttribute('aria-expanded', 'true');
    }

    function fetchSuggestions(query) {
        if (activeController) activeController.abort();
        activeController = new AbortController();

        const url = input.dataset.suggestUrl + '?q=' + encodeURIComponent(query);
        fetch(url, { signal: activeController.signal })
            .then(res => res.json())
            .then(data => {
                // A slower earlier request could resolve after a newer one;
                // only render if this response still matches the input's
                // current text.
                if (input.value.trim() === data.query) {
                    renderResults(data.query, data.results);
                }
            })
            .catch(function (err) {
                if (err.name !== 'AbortError') closePanel();
            });
    }

    input.addEventListener('input', function () {
        clearTimeout(debounceTimer);
        const query = input.value.trim();

        if (query.length < MIN_CHARS) {
            closePanel();
            return;
        }

        debounceTimer = setTimeout(function () {
            fetchSuggestions(query);
        }, DEBOUNCE_MS);
    });

    input.addEventListener('keydown', function (e) {
        if (panel.hidden) return;

        if (e.key === 'Escape') {
            closePanel();
        } else if (e.key === 'ArrowDown') {
            e.preventDefault();
            setActive(activeIndex + 1);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            setActive(activeIndex - 1);
        } else if (e.key === 'Enter' && activeIndex >= 0) {
            e.preventDefault();
            const list = items();
            if (list[activeIndex]) window.location.href = list[activeIndex].href;
        }
    });

    document.addEventListener('click', function (e) {
        if (!form.contains(e.target)) closePanel();
    });

    form.addEventListener('submit', closePanel);
});
