document.addEventListener('DOMContentLoaded', function () {

    function initSubmenus(root) {
        root.querySelectorAll('.dropdown-submenu').forEach(function (submenu) {
            let hideTimer;

            submenu.addEventListener('mouseenter', function () {
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
                hideTimer = setTimeout(function () {
                    const menu = submenu.querySelector(':scope > .dropdown-menu');
                    if (menu) menu.classList.remove('show');
                    // Also close all nested submenus inside
                    submenu.querySelectorAll('.dropdown-menu').forEach(m => m.classList.remove('show'));
                }, 150);
            });

            // Touch devices never fire mouseenter/mouseleave, so the submenu
            // above would otherwise be unreachable on mobile. Fall back to
            // tap-to-toggle when the device has no real hover capability.
            const toggle = submenu.querySelector(':scope > a');
            if (toggle) {
                toggle.addEventListener('click', function (e) {
                    if (!window.matchMedia('(hover: hover)').matches) {
                        e.preventDefault();
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
