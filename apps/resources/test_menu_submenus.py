"""Nested topic menus keep working after the header loads /menu/ lazily.

The category row is in the first HTML response. Its flyouts arrive
later and replace the nodes inside #siteCategoryMenu. Submenu hover
and tap are delegated from document, and a category opened while that
request is still in flight shows a loading row, then opens with the
real links.
"""
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from apps.resources.models import MenuItem

HEADER_JS = Path(__file__).resolve().parents[2] / 'static' / 'js' / 'header.js'
CHROME = shutil.which('google-chrome') or shutil.which('google-chrome-stable')
CANONICAL_ORIGIN = 'https://mathkg.com'


class MenuSubtreeTests(TestCase):
    def setUp(self):
        numbers = MenuItem.objects.create(title='Сандар', order=1)
        order = MenuItem.objects.create(title='Амалдардын тартиби', parent=numbers, order=1)
        MenuItem.objects.create(
            title='Төрт амал', parent=order, order=1, url_name='four_basic_operations',
        )
        geometry = MenuItem.objects.create(title='Геометрия', order=2)
        angles = MenuItem.objects.create(title='Бурчтар', parent=geometry, order=1)
        MenuItem.objects.create(
            title='Терминология',
            parent=angles,
            order=1,
            url_name='geometry_angles_angle_facts_vocabulary',
        )

    def test_home_is_shallow_and_the_fragment_has_the_flyouts(self):
        home = self.client.get(reverse('home')).content.decode()
        self.assertIn('Сандар', home)
        self.assertIn('Геометрия', home)
        self.assertNotIn('Амалдардын тартиби', home)
        self.assertNotIn('dropdown-submenu', home)
        self.assertIn('data-bs-auto-close="outside"', home)
        self.assertIn('header.js?v=20261102a', home)

        fragment = self.client.get(reverse('menu_fragment'))
        html = fragment.content.decode()
        self.assertEqual(fragment.status_code, 200)
        self.assertIn('dropdown-submenu', html)
        self.assertIn('Амалдардын тартиби', html)
        self.assertIn('/four_basic_operations/', html)
        self.assertIn('Терминология', html)
        self.assertIn('data-bs-auto-close="outside"', html)

    def test_topics_page_still_lists_the_whole_tree(self):
        html = self.client.get(reverse('topics_tree')).content.decode()
        tree = html.split('topics-tree', 1)[1]
        self.assertIn('Амалдардын тартиби', tree)
        self.assertIn('Төрт амал', tree)
        self.assertIn('/four_basic_operations/', tree)
        self.assertIn('Бурчтар', tree)
        self.assertIn('/geometry-angles-angle-facts-vocabulary/', tree)

    def test_sitemap_lists_topics_and_skips_the_menu_fragment(self):
        response = self.client.get(
            '/sitemap.xml', HTTP_HOST='mathkg.com', secure=True,
        )
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertIn(f'{CANONICAL_ORIGIN}/topics/', body)
        self.assertNotIn(f'{CANONICAL_ORIGIN}/menu/', body)
        self.assertNotIn('railway.app', body)

    def test_header_script_delegates_instead_of_binding_the_first_paint(self):
        source = HEADER_JS.read_text()
        self.assertIn("document.addEventListener('mouseover'", source)
        self.assertIn("document.addEventListener('mouseout'", source)
        self.assertIn("closest('.dropdown-submenu > a')", source)
        self.assertIn("closest('[data-bs-toggle=\"dropdown\"]')", source)
        self.assertNotIn("classList.contains('dropdown')", source)
        self.assertIn('Жүктөлүүдө', source)


class MenuSubmenuBrowserTests(SimpleTestCase):
    def test_delegated_submenus_open_on_hover_tap_and_after_injection(self):
        if not CHROME:
            self.skipTest('google-chrome is not installed')
        source = HEADER_JS.read_text()
        html = _harness(source)
        with tempfile.TemporaryDirectory() as folder:
            page = Path(folder) / 'menu.html'
            page.write_text(html, encoding='utf-8')
            dumped = _dump_dom(page)
        marker = 'data-submenu-test="'
        self.assertIn(marker, dumped, dumped[-2000:])
        result = dumped.split(marker, 1)[1].split('"', 1)[0]
        self.assertEqual(result, 'pass', result)


def _dump_dom(page):
    """Headless Chrome prints the DOM, then keeps running in this image.

    Read until the harness result is on the page, then stop the process.
    """
    proc = subprocess.Popen(
        [
            CHROME,
            '--headless=new',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--dump-dom',
            page.as_uri(),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    fd = proc.stdout.fileno()
    os.set_blocking(fd, False)
    data = b''
    deadline = time.time() + 20
    try:
        while time.time() < deadline:
            try:
                piece = os.read(fd, 65536)
            except BlockingIOError:
                piece = b''
            if piece:
                data += piece
                if b'data-submenu-test="' in data and b'</html>' in data:
                    break
            elif proc.poll() is not None:
                break
            else:
                time.sleep(0.05)
    finally:
        proc.kill()
        proc.wait(timeout=5)
    return data.decode()


def _harness(source):
    return """<!DOCTYPE html>
<html>
<body>
<div id="categoryNav">
  <ul id="siteCategoryMenu" data-menu-url="/menu/" data-loaded="1">
    <li class="nav-item dropdown">
      <a class="mymenu dropdown-toggle" href="#" data-bs-toggle="dropdown" aria-expanded="true"><span>Сандар</span></a>
      <ul class="dropdown-menu show">
        <li class="dropdown-submenu" id="order">
          <a href="#" class="dropdown-item"><span>Амалдардын тартиби</span></a>
          <ul class="dropdown-menu" id="order-menu">
            <li class="dropdown-leaf"><a href="/four_basic_operations/" id="four">Төрт амал</a></li>
          </ul>
        </li>
        <li class="dropdown-submenu" id="angles">
          <a href="#" class="dropdown-item"><span>Бурчтар</span></a>
          <ul class="dropdown-menu" id="angles-menu">
            <li class="dropdown-submenu" id="facts">
              <a href="#" class="dropdown-item"><span>Бурч фактылары</span></a>
              <ul class="dropdown-menu" id="facts-menu">
                <li class="dropdown-leaf"><a href="/geometry-angles-angle-facts-vocabulary/" id="term">Терминология</a></li>
              </ul>
            </li>
          </ul>
        </li>
      </ul>
    </li>
  </ul>
</div>
<script>
window.__forceNoHover = false;
window.__menuHTML = '';
(function () {
  var native = window.matchMedia.bind(window);
  window.matchMedia = function (query) {
    if (query === '(hover: hover)') {
      return {
        matches: !window.__forceNoHover,
        media: query,
        addEventListener: function () {},
        removeEventListener: function () {},
        addListener: function () {},
        removeListener: function () {}
      };
    }
    return native(query);
  };
})();
window.bootstrap = {
  Dropdown: class Dropdown {
    constructor(el, config) {
      this._element = el;
      this._config = { autoClose: (config && config.autoClose) || 'true' };
      el.__dd = this;
    }
    static getInstance(el) { return el.__dd || null; }
    static getOrCreateInstance(el, config) {
      return el.__dd || new this(el, config);
    }
    dispose() { this._element.__dd = null; }
    show() {
      var menu = this._element.parentElement.querySelector(':scope > .dropdown-menu');
      if (menu) menu.classList.add('show');
      this._element.setAttribute('aria-expanded', 'true');
      this._element.classList.add('show');
      this._element.dispatchEvent(new Event('shown.bs.dropdown', { bubbles: true }));
    }
  }
};
window.fetch = function () {
  return Promise.resolve({
    ok: true,
    text: function () { return Promise.resolve(window.__menuHTML); }
  });
};
</script>
<script>
""" + source + """
</script>
<script>
document.addEventListener('DOMContentLoaded', function () {
  var failures = [];
  function check(name, ok) { if (!ok) failures.push(name); }
  function finish(extra) {
    if (extra) failures.push(extra);
    document.documentElement.setAttribute('data-submenu-test', failures.length ? failures.join(' | ') : 'pass');
  }
  try {
    var order = document.getElementById('order');
    var orderMenu = document.getElementById('order-menu');
    var parentMenu = order.parentElement;
    order.querySelector('span').dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
    check('hover opens order', orderMenu.classList.contains('show'));
    check('parent stays open', parentMenu.classList.contains('show'));

    var click = new MouseEvent('click', { bubbles: true, cancelable: true });
    order.querySelector('a').dispatchEvent(click);
    check('submenu click prevented', click.defaultPrevented);
    check('click keeps flyout', orderMenu.classList.contains('show'));
    check('click keeps category', parentMenu.classList.contains('show'));

    var four = document.getElementById('four');
    var leafDefault = false;
    four.addEventListener('click', function (event) {
      leafDefault = event.defaultPrevented;
      event.preventDefault();
    });
    four.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
    check('topic link still clicks', !leafDefault);

    document.getElementById('angles').querySelector('a').dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
    document.getElementById('facts').querySelector('a').dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
    check('geometry section opens', document.getElementById('angles-menu').classList.contains('show'));
    check('nested geometry opens', document.getElementById('facts-menu').classList.contains('show'));

    var list = document.getElementById('siteCategoryMenu');
    list.innerHTML = '<li class="nav-item dropdown"><a class="mymenu dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="true"><span>Геометрия</span></a><ul class="dropdown-menu show"><li class="dropdown-submenu" id="injected"><a href="#"><span>Бурчтар</span></a><ul class="dropdown-menu" id="injected-menu"><li class="dropdown-leaf"><a href="/geometry-angles-angle-facts-vocabulary/">Терминология</a></li></ul></li></ul></li>';
    document.getElementById('injected').querySelector('a').dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
    check('injected submenu opens', document.getElementById('injected-menu').classList.contains('show'));

    window.__forceNoHover = true;
    var touchMenu = document.getElementById('injected-menu');
    touchMenu.classList.remove('show');
    var touchClick = new MouseEvent('click', { bubbles: true, cancelable: true });
    document.getElementById('injected').querySelector('span').dispatchEvent(touchClick);
    check('tap opens', touchMenu.classList.contains('show'));
    document.getElementById('injected').querySelector('span').dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
    check('second tap closes', !touchMenu.classList.contains('show'));
    window.__forceNoHover = false;

    delete list.dataset.loaded;
    delete list.dataset.loading;
    list.innerHTML = '<li class="nav-item dropdown"><a class="mymenu dropdown-toggle" href="#" data-bs-toggle="dropdown" aria-expanded="false"><span>Сандар</span></a><ul class="dropdown-menu"></ul></li>';
    window.__menuHTML = '<li class="nav-item dropdown"><a class="mymenu dropdown-toggle" href="#" data-bs-toggle="dropdown" aria-expanded="false"><span>Сандар</span></a><ul class="dropdown-menu"><li class="dropdown-submenu" id="late"><a href="#"><span>Амалдардын тартиби</span></a><ul class="dropdown-menu" id="late-menu"><li class="dropdown-leaf"><a href="/four_basic_operations/">Төрт амал</a></li></ul></li></ul></li>';
    document.getElementById('categoryNav').dispatchEvent(new Event('pointerenter'));
    window.bootstrap.Dropdown.getOrCreateInstance(list.querySelector('a.dropdown-toggle')).show();
    check('loading row', !!list.querySelector('.menu-loading'));
    check('loading copy', list.textContent.indexOf('Жүктөлүүдө') !== -1);

    Promise.resolve().then(function () { return Promise.resolve(); }).then(function () {
      try {
        check('loaded links', list.textContent.indexOf('Төрт амал') !== -1);
        check('loading gone', !list.querySelector('.menu-loading'));
        check('category reopened', list.querySelector(':scope > .dropdown > .dropdown-menu').classList.contains('show'));
        document.getElementById('late').querySelector('a').dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
        check('late submenu opens', document.getElementById('late-menu').classList.contains('show'));
        finish();
      } catch (err) { finish(String(err)); }
    });
  } catch (err) { finish(String(err)); }
});
</script>
</body>
</html>
"""
