/* Keeps a .mk-zoom graphic inside the viewport when it scales.
   The scale comes from --mk-zoom-scale (1.3). Sets --mk-zoom-origin before
   hover. No effect when the device cannot hover. */
(function () {
    if (!window.matchMedia("(hover: hover)").matches) return;

    var nodes = function () {
        return document.querySelectorAll(".mk-zoom");
    };

    function scaleOf(el) {
        var raw = window.getComputedStyle(el).getPropertyValue("--mk-zoom-scale");
        var scale = parseFloat(raw);
        return scale > 1 ? scale : 1.3;
    }

    function axis(start, size, limit, scale) {
        var span = (scale - 1) * size;
        var min = (start + scale * size - limit) / span;
        var max = start / span;
        if (min <= max) {
            var lo = Math.max(0, Math.min(1, min));
            var hi = Math.max(0, Math.min(1, max));
            if (lo <= hi) {
                if (0.5 >= lo && 0.5 <= hi) return 0.5;
                return Math.abs(lo - 0.5) < Math.abs(hi - 0.5) ? lo : hi;
            }
        }
        // Too big to fit. Keep the near edge inside and grow toward the middle.
        return Math.max(0, Math.min(1, max));
    }

    function topInset() {
        var bar = document.querySelector(".fixed-top");
        if (!bar) return 0;
        var bottom = bar.getBoundingClientRect().bottom;
        return bottom > 0 ? bottom : 0;
    }

    function place(el) {
        if (window.getComputedStyle(el).transform !== "none") return;
        var r = el.getBoundingClientRect();
        if (!r.width || !r.height) return;
        var inset = topInset() + 16;
        var scale = scaleOf(el);
        var ox = axis(r.left - 8, r.width, document.documentElement.clientWidth - 16, scale);
        var oy = axis(r.top - inset, r.height, window.innerHeight - inset - 8, scale);
        el.style.setProperty("--mk-zoom-origin", (ox * 100) + "% " + (oy * 100) + "%");
    }

    function placeAll() {
        nodes().forEach(place);
    }

    placeAll();
    window.addEventListener("scroll", placeAll, { passive: true });
    window.addEventListener("resize", placeAll);
    document.addEventListener("pointerover", function (event) {
        var el = event.target.closest && event.target.closest(".mk-zoom");
        if (!el) return;
        place(el);
        el.dataset.mkZoomOpen = "1";
    }, true);
    document.addEventListener("pointerout", function (event) {
        var el = event.target.closest && event.target.closest(".mk-zoom");
        if (!el) return;
        if (event.relatedTarget && el.contains(event.relatedTarget)) return;
        delete el.dataset.mkZoomOpen;
    }, true);
    document.addEventListener("focusin", function (event) {
        if (event.target.classList && event.target.classList.contains("mk-zoom")) {
            place(event.target);
            event.target.dataset.mkZoomOpen = "1";
        }
    });
    document.addEventListener("focusout", function (event) {
        if (event.target.classList && event.target.classList.contains("mk-zoom")) {
            delete event.target.dataset.mkZoomOpen;
        }
    });
})();
