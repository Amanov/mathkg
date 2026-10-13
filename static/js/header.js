document.addEventListener('DOMContentLoaded', function () {

    // A long panel (many items) can be taller than the space left below
    // where it opens - without this, its bottom items are simply cut off
    // past the screen edge with no way to reach them. Caps it to whatever
    // vertical room is actually available and lets it scroll internally
    // instead. Shared by the root dropdown and its flyout submenus.
    function capHeightToViewport(menu) {
        const rect = menu.getBoundingClientRect();
        const available = window.innerHeight - 10 - rect.top;
        if (rect.height > available) {
            menu.style.maxHeight = `${Math.max(available, 100)}px`;
            menu.style.overflowY = 'auto';
            // overflow-y: auto forces overflow-x to compute as auto too
            // (CSS can't have one axis visible and the other not), which
            // would clip any flyout escaping to the right of this panel -
            // transform also has to go, since it (even at scale(1)) makes
            // this panel the containing block for a position: fixed
            // descendant, pinning a "fixed" flyout to its clipped box
            // instead of letting it escape to the viewport. Flagged via
            // data-capped so a flyout opening inside here (below) knows to
            // switch to fixed positioning instead of the normal relative one.
            menu.style.transform = 'none';
            menu.dataset.capped = 'true';
        } else {
            menu.style.maxHeight = '';
            menu.style.overflowY = '';
            menu.style.transform = '';
            delete menu.dataset.capped;
        }
    }

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

                // Reset before measuring so a previous open's position
                // (possibly computed at a different window size) never
                // contaminates this measurement. Clearing 'right' to ''
                // (not 'auto') matters: an inline 'auto' is still an inline
                // value, so it permanently outranks the stylesheet's own
                // `right: calc(100% + 6px)` on .dropstart - once set here,
                // no later flip could ever move the flyout again, which is
                // what collapsed it back onto its own trigger's static
                // position and read as the panel overlapping its ancestor.
                menu.style.position = '';
                menu.style.top = '';
                menu.style.left = '';
                menu.style.right = '';
                menu.style.transform = '';
                menu.style.transition = '';
                menu.style.maxHeight = '';
                menu.style.overflowY = '';
                submenu.classList.remove('dropstart');

                menu.classList.add('show');

                // A panel this opens inside of may itself be scrolling
                // (capHeightToViewport above, applied to a tall top-level
                // category) - its overflow: auto clips anything escaping
                // its box, including this flyout's normal position:
                // absolute/right-of-trigger placement. Pin it to the
                // viewport with fixed, computed coordinates instead, which
                // escapes that clipping the same way capHeightToViewport
                // already drops this ancestor's transform to allow.
                const cappedAncestor = submenu.closest('.dropdown-menu[data-capped="true"]');
                if (cappedAncestor) {
                    // position: fixed is positioned relative to the viewport
                    // UNLESS some ancestor has a transform (even a no-op
                    // one like scale(1)), in which case THAT ancestor
                    // becomes the containing block instead - silently
                    // turning "fixed, viewport-relative" into "fixed,
                    // relative to whichever transformed box happens to be
                    // nearest". Every .dropdown-menu carries a transform by
                    // default (the open/close scale animation), including
                    // ordinary uncapped ones this flyout may be nested
                    // inside - clearing only the matched capped ancestor's
                    // transform isn't enough if a closer, uncapped one sits
                    // between it and this flyout. Clear every ancestor
                    // panel's transform, not just the capped one, so this
                    // is reliably viewport-relative regardless of depth.
                    // Harmless to leave cleared: translateY(0) scale(1) is
                    // the identity transform, so this never changes how
                    // any ancestor itself looks.
                    let ancestorMenu = submenu.parentElement && submenu.parentElement.closest('.dropdown-menu');
                    while (ancestorMenu) {
                        ancestorMenu.style.transform = 'none';
                        ancestorMenu = ancestorMenu.parentElement && ancestorMenu.parentElement.closest('.dropdown-menu');
                    }

                    // .dropdown-menu's stylesheet transition covers
                    // transform (the open/close scale animation) - setting
                    // transform: none above doesn't jump there instantly,
                    // it transitions toward it over --transition-base
                    // (200ms). Every getBoundingClientRect() read below,
                    // taken synchronously, would land mid-transition and
                    // report an interpolated (wrong) box - which the flip/
                    // fit checks below would then act on, baking a bad
                    // decision (e.g. flipping to the left edge when there
                    // was no overflow to begin with) into inline styles
                    // that never get revisited once the transition actually
                    // finishes. Killing the transition up front makes
                    // every measurement from here on reflect the real,
                    // final geometry immediately.
                    menu.style.transition = 'none';

                    const triggerRect = submenu.getBoundingClientRect();
                    menu.style.position = 'fixed';
                    menu.style.transform = 'none';
                    menu.style.top = `${triggerRect.top}px`;
                    menu.style.left = `${triggerRect.right - 1.5}px`;
                    menu.style.right = 'auto';

                    const rect = menu.getBoundingClientRect();
                    if (rect.right > window.innerWidth - 10) {
                        menu.style.left = `${Math.max(10, triggerRect.left - rect.width + 1.5)}px`;
                    }
                    // Shifting up to fit must never go higher than the
                    // capped ancestor's own top - that panel already sits
                    // below the fixed header (Bootstrap positioned it
                    // there), so this stays below the header too. A flat
                    // 10px-from-viewport-top floor doesn't know the header
                    // exists and tucks this flyout's first rows underneath
                    // it, unreachable.
                    const afterFlipRect = menu.getBoundingClientRect();
                    if (afterFlipRect.bottom > window.innerHeight - 10) {
                        const minTop = cappedAncestor.getBoundingClientRect().top;
                        const shiftedTop = Math.max(minTop, window.innerHeight - 10 - afterFlipRect.height);
                        menu.style.top = `${shiftedTop}px`;
                    }
                    capHeightToViewport(menu);
                    return;
                }

                // Flip left if off right edge
                const rect = menu.getBoundingClientRect();
                if (rect.right > window.innerWidth - 10) {
                    submenu.classList.add('dropstart');
                }

                // Shift up if off bottom edge, but never further than the
                // top of this menu's own parent column - beyond that the
                // flyout rises above the level that contains it, which is
                // what reads as the panels overlapping each other.
                if (rect.bottom > window.innerHeight - 10 && submenu.parentElement) {
                    const desiredShift = rect.bottom - window.innerHeight + 10;
                    const parentMenuTop = submenu.parentElement.getBoundingClientRect().top;
                    const maxShift = Math.max(0, rect.top - parentMenuTop);
                    const shift = Math.min(desiredShift, maxShift);
                    const currentTop = parseFloat(getComputedStyle(menu).top) || 0;
                    menu.style.top = `${currentTop - shift}px`;
                }

                // Still taller than the viewport even after shifting up as
                // far as the ancestor boundary allows - cap and scroll.
                capHeightToViewport(menu);
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

            // The root panel itself can be taller than the room left below
            // it (e.g. a category with a dozen+ children) - same reachability
            // problem as a tall flyout, same fix.
            const menu = dropdown.querySelector(':scope > .dropdown-menu');
            if (menu) capHeightToViewport(menu);
        });
        // Also close all submenus when root dropdown closes, and clear any
        // height cap so the next open re-measures fresh (the viewport may
        // have been resized, or this dropdown opened from a different
        // scroll position, since the last time it was shown).
        dropdown.addEventListener('hidden.bs.dropdown', function () {
            dropdown.querySelectorAll('.dropdown-menu').forEach(function (m) {
                m.classList.remove('show');
                m.style.maxHeight = '';
                m.style.overflowY = '';
                m.style.transform = '';
                m.style.position = '';
                m.style.transition = '';
                delete m.dataset.capped;
            });
        });
    });

});
