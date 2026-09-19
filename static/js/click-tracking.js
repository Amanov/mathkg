// Logs a click on anything with data-track="<label>" so the analytics
// dashboard can show which buttons/links get used the most. One delegated
// listener instead of per-button handlers, so any new data-track element
// just works without extra wiring.
(function () {
    document.addEventListener('click', function (event) {
        var target = event.target.closest('[data-track]');
        if (!target) {
            return;
        }

        var payload = JSON.stringify({
            label: target.getAttribute('data-track'),
            path: window.location.pathname,
        });

        if (navigator.sendBeacon) {
            navigator.sendBeacon('/track-click/', payload);
        } else {
            fetch('/track-click/', {
                method: 'POST',
                body: payload,
                keepalive: true,
            }).catch(function () {});
        }
    });
})();
