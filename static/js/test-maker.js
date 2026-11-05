(function () {
    var grade = document.getElementById('id_grade');
    var list = document.getElementById('id_topics');
    var hint = document.getElementById('test-available');
    if (!grade || !list) return;
    var boxes = list.querySelectorAll('input[type="checkbox"]');

    function parseCounts(value) {
        var map = {};
        (value || '').split(',').forEach(function (part) {
            var bits = part.split(':');
            if (bits.length === 2) map[bits[0]] = parseInt(bits[1], 10) || 0;
        });
        return map;
    }

    function apply() {
        var selected = grade.value;
        var total = 0;
        boxes.forEach(function (box) {
            var counts = parseCounts(box.getAttribute('data-counts'));
            var item = box.closest('li') || box.parentElement.parentElement;
            var show = Object.prototype.hasOwnProperty.call(counts, selected);
            if (item) item.hidden = !show;
            if (!show) box.checked = false;
            if (show && box.checked) total += counts[selected] || 0;
        });
        if (hint) {
            hint.textContent = total
                ? 'Тандалган темаларда ' + total + ' суроо бар.'
                : 'Теманы белгилеңиз.';
        }
    }

    grade.addEventListener('change', apply);
    boxes.forEach(function (box) {
        box.addEventListener('change', apply);
    });
    apply();
})();
