document.addEventListener('DOMContentLoaded', function () {

    function initSubmenus(root) {
        root.querySelectorAll('.dropdown-submenu').forEach(function (submenu) {
            // shown.bs.dropdown fires every time the parent dropdown opens;
            // guard so re-opening it doesn't stack duplicate listeners.
            if (submenu.dataset.submenuBound) return;
            submenu.dataset.submenuBound = 'true';

            let hideTimer;

            submenu.addEventListener('mouseenter', function () {
                // A tap on a touchscreen fires a synthetic mouseenter right
                // before its click event, which would open this via hover
                // and then have the click handler below immediately toggle
                // it shut again on the very same tap. Hover-open is for
                // real pointers only; touch uses the click handler instead.
                if (!window.matchMedia('(hover: hover)').matches) return;

                clearTimeout(hideTimer);

                // Close siblings at the same level
                if (submenu.parentElement) {
                    submenu.parentElement
                        .querySelectorAll(':scope > .dropdown-submenu > .dropdown-menu')
                        .forEach(s => s.classList.remove('show'));
                }

                const menu = submenu.querySelector(':scope > .dropdown-menu');
                if (!menu) return;

                menu.classList.add('show');

                // Flip left if off right edge
                const rect = menu.getBoundingClientRect();
                if (rect.right > window.innerWidth - 10) {
                    submenu.classList.add('dropstart');
                } else {
                    submenu.classList.remove('dropstart');
                    menu.style.left = '';
                    menu.style.right = 'auto';
                }

                // Shift up if off bottom edge
                if (rect.bottom > window.innerHeight - 10) {
                    menu.style.top = `-${rect.bottom - window.innerHeight + 10}px`;
                } else {
                    menu.style.top = '';
                }
            });

            submenu.addEventListener('mouseleave', function () {
                if (!window.matchMedia('(hover: hover)').matches) return;

                hideTimer = setTimeout(function () {
                    const menu = submenu.querySelector(':scope > .dropdown-menu');
                    if (menu) menu.classList.remove('show');
                    // Also close all nested submenus inside
                    submenu.querySelectorAll('.dropdown-menu').forEach(m => m.classList.remove('show'));
                }, 150);
            });

            // This toggle is a submenu opener, not a real link (href="#") — a
            // click on it must never reach Bootstrap's document-level
            // auto-close listener, which otherwise treats any click inside
            // the open dropdown as a reason to close the whole thing,
            // instantly hiding the submenu we're trying to reveal. This is
            // also what breaks it on desktop: hover opens the flyout, but a
            // stray click on the toggle closes the entire top-level menu.
            const toggle = submenu.querySelector(':scope > a');
            if (toggle) {
                toggle.addEventListener('click', function (e) {
                    e.preventDefault();
                    e.stopPropagation();

                    // Touch devices never fire mouseenter/mouseleave, so tap
                    // has to do the opening/closing that hover does elsewhere.
                    if (!window.matchMedia('(hover: hover)').matches) {
                        const menu = submenu.querySelector(':scope > .dropdown-menu');
                        if (!menu) return;
                        const isOpen = menu.classList.contains('show');

                        if (submenu.parentElement) {
                            submenu.parentElement
                                .querySelectorAll(':scope > .dropdown-submenu > .dropdown-menu')
                                .forEach(s => s.classList.remove('show'));
                        }

                        menu.classList.toggle('show', !isOpen);
                    }
                });
            }
        });
    }

    // Init on root dropdown open
    document.querySelectorAll('.dropdown').forEach(function (dropdown) {
        dropdown.addEventListener('shown.bs.dropdown', function () {
            initSubmenus(dropdown);
        });
        // Also close all submenus when root dropdown closes
        dropdown.addEventListener('hidden.bs.dropdown', function () {
            dropdown.querySelectorAll('.dropdown-menu').forEach(m => m.classList.remove('show'));
        });
    });

});
