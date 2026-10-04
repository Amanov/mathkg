document.addEventListener('DOMContentLoaded', function () {
    var btn = document.getElementById('themeToggle');
    if (!btn) return;

    btn.addEventListener('click', function () {
        var html = document.documentElement;
        var isDark = html.getAttribute('data-theme') === 'dark';
        var next = isDark ? 'light' : 'dark';

        html.setAttribute('data-theme', next);
        html.setAttribute('data-bs-theme', next);

        try {
            localStorage.setItem('mathkg-theme', next);
        } catch (e) {}
    });
});
