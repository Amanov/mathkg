document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('subscribeModal');
    if (!modal) return;

    const planStep = document.getElementById('subscribePlanStep');
    const qrStep = document.getElementById('subscribeQrStep');
    const backBtn = document.getElementById('subscribeBackBtn');
    const continueBtn = document.getElementById('subscribeContinueBtn');
    const nameEl = document.getElementById('subscribeSelectedPlanName');
    const priceEl = document.getElementById('subscribeSelectedPlanPrice');
    const registerUrl = continueBtn.getAttribute('href');

    modal.querySelectorAll('.subscribe-plan-card').forEach(function (card) {
        card.addEventListener('click', function () {
            const plan = card.dataset.plan;
            nameEl.textContent = card.querySelector('.subscribe-plan-name').textContent;
            priceEl.textContent = card.dataset.price;
            continueBtn.setAttribute('href', registerUrl + '?plan=' + encodeURIComponent(plan));
            planStep.classList.add('d-none');
            qrStep.classList.remove('d-none');
        });
    });

    backBtn.addEventListener('click', function () {
        qrStep.classList.add('d-none');
        planStep.classList.remove('d-none');
    });

    // Reset to the plan-picking step every time the modal is reopened,
    // so a previous visit's QR view doesn't linger.
    modal.addEventListener('hidden.bs.modal', function () {
        qrStep.classList.add('d-none');
        planStep.classList.remove('d-none');
    });
});
