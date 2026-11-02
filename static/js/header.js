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

    // The full menu arrives after the first paint and replaces every
    // node inside #siteCategoryMenu. Listeners bound to those nodes
    // (or only when shown.bs.dropdown's target happens to be the
    // <li class="dropdown">) never see the injected submenus. Bootstrap
    // fires shown/hidden on the toggle <a>, which then bubbles.
    // Delegation on document keeps hover, click, and tap working for
    // whatever HTML is in the menu at that moment.
    const hideTimers = new WeakMap();

    function canHover() {
        return window.matchMedia('(hover: hover)').matches;
    }

    function submenuFrom(target) {
        if (!target || !target.closest) return null;
        const submenu = target.closest('.dropdown-submenu');
        if (!submenu || !submenu.closest('#siteCategoryMenu')) return null;
        return submenu;
    }

    function parentMenuVisible(submenu) {
        const parentMenu = submenu.parentElement && submenu.parentElement.closest('.dropdown-menu');
        return !!(parentMenu && parentMenu.classList.contains('show'));
    }

    function categoryTitle(toggle) {
        const label = toggle.querySelector('span');
        return (label ? label.textContent : toggle.textContent).replace(/\s+/g, ' ').trim();
    }

    function rootDropdown(event) {
        const toggle = event.target && event.target.closest
            ? event.target.closest('[data-bs-toggle="dropdown"]')
            : null;
        if (!toggle) return null;
        const dropdown = toggle.closest('.dropdown');
        if (!dropdown || !dropdown.closest('#siteCategoryMenu')) return null;
        return { toggle: toggle, dropdown: dropdown };
    }

    function cancelClose(submenu) {
        const timer = hideTimers.get(submenu);
        if (!timer) return;
        clearTimeout(timer);
        hideTimers.delete(submenu);
    }

    function closeSubmenu(submenu) {
        submenu.querySelectorAll('.dropdown-menu').forEach(function (menu) {
            menu.classList.remove('show');
        });
    }

    function scheduleClose(submenu) {
        cancelClose(submenu);
        hideTimers.set(submenu, setTimeout(function () {
            hideTimers.delete(submenu);
            closeSubmenu(submenu);
        }, 150));
    }

    function openSubmenu(submenu) {
        cancelClose(submenu);

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
    }

    function toggleTouchSubmenu(submenu) {
        const menu = submenu.querySelector(':scope > .dropdown-menu');
        if (!menu) return;
        const isOpen = menu.classList.contains('show');

        if (submenu.parentElement) {
            submenu.parentElement
                .querySelectorAll(':scope > .dropdown-submenu > .dropdown-menu')
                .forEach(s => s.classList.remove('show'));
        }

        menu.classList.toggle('show', !isOpen);
        if (!isOpen) return;
        menu.querySelectorAll('.dropdown-menu').forEach(function (nested) {
            nested.classList.remove('show');
        });
    }

    // mouseenter does not bubble, so a document listener cannot see it.
    // mouseover does, and the relatedTarget check makes it enter-only.
    document.addEventListener('mouseover', function (event) {
        if (!canHover()) return;
        const submenu = submenuFrom(event.target);
        if (!submenu) return;
        if (event.relatedTarget && submenu.contains(event.relatedTarget)) return;
        if (!parentMenuVisible(submenu)) return;
        openSubmenu(submenu);
    });

    document.addEventListener('mouseout', function (event) {
        if (!canHover()) return;
        let submenu = submenuFrom(event.target);
        while (submenu) {
            if (event.relatedTarget && submenu.contains(event.relatedTarget)) break;
            scheduleClose(submenu);
            submenu = submenu.parentElement && submenu.parentElement.closest('.dropdown-submenu');
        }
    });

    // Capture runs before Bootstrap's document click listener, which
    // closes a dropdown on any click inside it. The toggle is href="#",
    // so the click must not navigate either. stopPropagation keeps the
    // category open; the beacon below is what click-tracking.js would
    // have sent on the bubble that no longer arrives.
    document.addEventListener('click', function (event) {
        const toggle = event.target && event.target.closest
            ? event.target.closest('.dropdown-submenu > a')
            : null;
        if (!toggle || !toggle.closest('#siteCategoryMenu')) return;
        event.preventDefault();
        event.stopPropagation();

        const label = toggle.getAttribute('data-track');
        if (label && navigator.sendBeacon) {
            navigator.sendBeacon('/track-click/', JSON.stringify({
                label: label,
                path: window.location.pathname,
            }));
        }

        const submenu = toggle.parentElement;
        if (!submenu || !submenu.classList.contains('dropdown-submenu')) return;
        if (!parentMenuVisible(submenu)) return;
        if (canHover()) {
            const menu = submenu.querySelector(':scope > .dropdown-menu');
            if (menu && !menu.classList.contains('show')) openSubmenu(submenu);
            return;
        }
        toggleTouchSubmenu(submenu);
    }, true);

    function showMenuLoading(dropdown) {
        const list = document.getElementById('siteCategoryMenu');
        if (!list || list.dataset.loaded === '1') return;
        const menu = dropdown.querySelector(':scope > .dropdown-menu');
        if (!menu || menu.querySelector('.dropdown-submenu, .dropdown-leaf, .menu-loading')) return;
        menu.innerHTML = '<li class="menu-loading" role="status">Жүктөлүүдө…</li>';
    }

    function keepSubmenusInside(toggle) {
        if (!window.bootstrap || !window.bootstrap.Dropdown) return;
        const instance = window.bootstrap.Dropdown.getInstance(toggle);
        if (instance && instance._config && instance._config.autoClose !== 'outside') {
            instance._config.autoClose = 'outside';
        }
    }

    document.addEventListener('shown.bs.dropdown', function (event) {
        const found = rootDropdown(event);
        if (!found) return;
        keepSubmenusInside(found.toggle);
        const list = document.getElementById('siteCategoryMenu');
        if (list) loadFullMenu(list);
        showMenuLoading(found.dropdown);

        // The root panel itself can be taller than the room left below
        // it (e.g. a category with a dozen+ children) - same reachability
        // problem as a tall flyout, same fix.
        const menu = found.dropdown.querySelector(':scope > .dropdown-menu');
        if (menu) capHeightToViewport(menu);
    });

    // Close every nested panel when the category closes, and clear any
    // height cap so the next open re-measures fresh (the viewport may
    // have been resized, or this dropdown opened from a different
    // scroll position, since the last time it was shown).
    document.addEventListener('hidden.bs.dropdown', function (event) {
        const found = rootDropdown(event);
        if (!found) return;
        found.dropdown.querySelectorAll('.dropdown-menu').forEach(function (m) {
            m.classList.remove('show');
            m.style.maxHeight = '';
            m.style.overflowY = '';
            m.style.transform = '';
            m.style.position = '';
            m.style.transition = '';
            delete m.dataset.capped;
        });
    });

    const list = document.getElementById('siteCategoryMenu');
    if (list && list.dataset.menuUrl) {
        const start = function () { loadFullMenu(list); };
        const nav = document.getElementById('categoryNav');
        if (nav) {
            nav.addEventListener('pointerenter', start);
            nav.addEventListener('focusin', start);
        }
        const toggler = document.querySelector('.navbar-toggler');
        if (toggler) toggler.addEventListener('pointerdown', start);
    }

    function reopenCategory(menuList, title) {
        const toggles = menuList.querySelectorAll(':scope > .dropdown > a.dropdown-toggle');
        for (const toggle of toggles) {
            if (categoryTitle(toggle) !== title) continue;
            if (window.bootstrap && window.bootstrap.Dropdown) {
                window.bootstrap.Dropdown.getOrCreateInstance(toggle, {
                    autoClose: 'outside',
                }).show();
            } else {
                const menu = toggle.parentElement.querySelector(':scope > .dropdown-menu');
                if (menu) menu.classList.add('show');
                toggle.setAttribute('aria-expanded', 'true');
            }
            return;
        }
    }

    function applyFullMenu(html) {
        const menuList = document.getElementById('siteCategoryMenu');
        if (!menuList || menuList.dataset.loaded === '1') return;

        const openToggle = menuList.querySelector('a.dropdown-toggle[aria-expanded="true"]');
        const openTitle = openToggle ? categoryTitle(openToggle) : '';
        if (openToggle && window.bootstrap && window.bootstrap.Dropdown) {
            const instance = window.bootstrap.Dropdown.getInstance(openToggle);
            if (instance) instance.dispose();
        }

        menuList.innerHTML = html;
        menuList.dataset.loaded = '1';
        delete menuList.dataset.loading;
        menuList.removeAttribute('aria-busy');
        if (openTitle) reopenCategory(menuList, openTitle);
    }

    function loadFullMenu(menuList) {
        if (!menuList || menuList.dataset.loaded === '1' || menuList.dataset.loading === '1') return;
        if (!menuList.dataset.menuUrl) return;
        menuList.dataset.loading = '1';
        menuList.setAttribute('aria-busy', 'true');
        fetch(menuList.dataset.menuUrl, {credentials: 'same-origin'})
            .then(function (response) {
                if (!response.ok) throw new Error('menu');
                return response.text();
            })
            .then(applyFullMenu)
            .catch(function () {
                delete menuList.dataset.loading;
                menuList.removeAttribute('aria-busy');
                const openMenu = menuList.querySelector('.dropdown-menu.show');
                if (openMenu && !openMenu.querySelector('.dropdown-submenu, .dropdown-leaf')) {
                    openMenu.innerHTML = '<li class="menu-loading" role="status">Меню жүктөлбөй калды. Дагы бир жолу ачыңыз.</li>';
                }
            });
    }

});
