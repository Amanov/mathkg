document.addEventListener('DOMContentLoaded', function () {
    var form = document.querySelector('.page-reaction__form');
    if (!form || !window.fetch) return;

    form.addEventListener('click', function (event) {
        var button = event.target.closest('button[name="face"]');
        if (!button || form.dataset.sending === '1') return;
        event.preventDefault();
        form.dataset.sending = '1';

        var body = new FormData(form);
        body.set('face', button.value);
        var tokenInput = form.querySelector('[name=csrfmiddlewaretoken]');
        var headers = { 'X-Requested-With': 'fetch' };
        if (tokenInput) headers['X-CSRFToken'] = tokenInput.value;

        fetch(form.action, {
            method: 'POST',
            body: body,
            credentials: 'same-origin',
            headers: headers,
        }).then(function (response) {
            if (!response.ok) throw new Error('reaction');
            var note = document.createElement('p');
            note.className = 'page-reaction__thanks';
            note.setAttribute('role', 'status');
            note.textContent = 'Рахмат!';
            form.replaceWith(note);
        }).catch(function () {
            delete form.dataset.sending;
            var input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'face';
            input.value = button.value;
            form.appendChild(input);
            form.submit();
        });
    });
});
