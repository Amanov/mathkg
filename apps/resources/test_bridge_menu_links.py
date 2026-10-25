"""Menu rows for nine bridge pages.

The migration looks parents up by title path and only runs when a menu
already exists, so the empty test database stays empty. These tests build
a small tree, including repeated titles under other parents, and call the
migration functions directly.
"""

import importlib

from django.test import TestCase
from django.urls import reverse

from apps.resources.models import MenuItem

links = importlib.import_module('apps.resources.migrations.0039_bridge_menu_links')


def _node(title, parent=None, order=0, url_name=None, slug=None):
    return MenuItem.objects.create(
        title=title,
        parent=parent,
        order=order,
        url_name=url_name,
        slug=slug,
    )


def _titles(parent):
    return list(
        MenuItem.objects.filter(parent=parent).order_by('order', 'pk').values_list('title', 'order')
    )


class BridgeMenuLinkTests(TestCase):
    def _tree(self):
        sandar = _node('Сандар', order=0)
        butun = _node('Бүтүн сандар', sandar, order=0)
        place = _node('Бүтүн сандардын орун наркы жана иреттөө', butun, order=0)
        words = _node('Бүтүн сандарды сөз менен туюнтуу', butun, order=1)
        arith = _node('Эсептөөлөр: 1 жана 2 орундук', butun, order=2)
        koshuu = _node('Кошуу', arith, order=0, url_name='integers_adding_1_2_digit')
        kemituu = _node('Кемитүү', arith, order=1)
        other_arith = _node('Эсептөөлөр: 2 жана 3 орундук', butun, order=3)
        decoy_koshuu = _node('Кошуу', other_arith, order=4, url_name='integers_adding_2_3_digit')
        real = _node('Турмуштук маселелер', butun, order=4)
        _node('Калькулятор менен', real, order=5)
        _node('Калькуляторсуз', real, order=6)
        _node('Рим сандарын окуу жана жазуу', butun, order=7)

        # Same titles, different branch. The path walk must not use these.
        decoy_intro = _node('Киришүү', sandar, order=9)
        decoy_def = _node('Аныктамалар', decoy_intro, order=0)

        prop = _node('Пропорция', order=1)
        ratio = _node('Катыш', prop, order=0)
        manip = _node('Өзгөртүп түзүү', ratio, order=0)
        _node('1:n', manip, order=2)
        _node('Өзгөртүү', manip, order=8)

        algebra = _node('Алгебра', order=2)
        intro = _node('Киришүү', algebra, order=0)
        _node('Аныктамалар', intro, order=0)
        _node('Белгилөөлөр', intro, order=1)
        equations = _node('Теңдемелер: сызыктуу', algebra, order=1)
        _node('Түзүү', equations, order=10)
        _node('Белгисиз бир жагында: калькулятор менен', equations, order=11)
        _node('Белгисиз бир жагында: калькуляторсуз', equations, order=12)
        algebra_manip = _node('Өзгөртүп түзүү', algebra, order=2)
        notation = _node('Белгилөө', algebra_manip, order=0)
        _node('Кошуу', notation, order=0)
        _node('Туюнтма түзүү', algebra_manip, order=1)

        return {
            'butun': butun,
            'arith': arith,
            'real': real,
            'manip': manip,
            'intro': intro,
            'equations': equations,
            'algebra_manip': algebra_manip,
            'decoy_koshuu': decoy_koshuu,
            'decoy_def': decoy_def,
            'place': place,
            'words': words,
            'koshuu': koshuu,
            'kemituu': kemituu,
        }

    def test_empty_menu_is_left_alone(self):
        links._add_links(MenuItem)
        links._remove_links(MenuItem)
        self.assertEqual(MenuItem.objects.count(), 0)
        self.assertNotIn('heuristics', [spec['url_name'] for spec in links.LINKS])

    def test_places_nine_rows_once_and_reverse_restores_orders(self):
        nodes = self._tree()
        before = list(
            MenuItem.objects.order_by('pk').values_list(
                'pk', 'parent_id', 'title', 'order', 'url_name', 'slug',
            )
        )

        links._add_links(MenuItem)
        once = list(
            MenuItem.objects.order_by('pk').values_list(
                'pk', 'parent_id', 'title', 'order', 'url_name', 'slug',
            )
        )
        links._add_links(MenuItem)
        self.assertEqual(
            list(MenuItem.objects.order_by('pk').values_list(
                'pk', 'parent_id', 'title', 'order', 'url_name', 'slug',
            )),
            once,
        )

        self.assertEqual(
            [title for title, _order in _titles(nodes['butun'])[:3]],
            [
                'Он көзөнөктүү рамка',
                'Сан курамы',
                'Бүтүн сандардын орун наркы жана иреттөө',
            ],
        )
        self.assertEqual(
            [title for title, _order in _titles(nodes['arith'])[:3]],
            ['Бөлүк–бүтүн тилке', 'Салыштыруу тилкеси', 'Кошуу'],
        )
        self.assertEqual(
            [title for title, _order in _titles(nodes['real'])],
            ['Калькулятор менен', 'Калькуляторсуз', 'Тилке модели'],
        )
        self.assertEqual(
            [title for title, _order in _titles(nodes['manip'])][-2:],
            ['Өзгөртүү', 'Мурун–кийин'],
        )
        self.assertEqual(
            [title for title, _order in _titles(nodes['intro'])[:2]],
            ['Тилкеден x ке', 'Аныктамалар'],
        )
        self.assertEqual(
            [title for title, _order in _titles(nodes['equations'])[:3]],
            ['Түзүү', 'Тараза ыкмасы', 'Белгисиз бир жагында: калькулятор менен'],
        )
        self.assertEqual(
            [title for title, _order in _titles(nodes['algebra_manip'])[:2]],
            ['Алгебралык плиткалар', 'Белгилөө'],
        )

        added = MenuItem.objects.filter(url_name__in=[spec['url_name'] for spec in links.LINKS])
        self.assertEqual(added.count(), 9)
        self.assertFalse(MenuItem.objects.filter(url_name='heuristics').exists())
        for spec in links.LINKS:
            row = MenuItem.objects.get(url_name=spec['url_name'])
            self.assertEqual(row.title, spec['title'])
            self.assertIsNone(row.slug)
            self.assertIsNone(row.topic_id)
            self.assertEqual(reverse(spec['url_name']), reverse(row.url_name))
        self.assertEqual(reverse('heuristics'), '/heuristics/')

        nodes['decoy_koshuu'].refresh_from_db()
        nodes['decoy_def'].refresh_from_db()
        self.assertEqual(nodes['decoy_koshuu'].order, 4)
        self.assertEqual(nodes['decoy_def'].order, 0)
        self.assertEqual(nodes['decoy_def'].parent.title, 'Киришүү')
        self.assertEqual(nodes['decoy_def'].parent.parent.title, 'Сандар')

        # A field that does not decide the link is cleared without a second shift.
        row = MenuItem.objects.get(url_name='san_kuramy')
        row.slug = 'not-the-link'
        row.save(update_fields=['slug'])
        links._add_links(MenuItem)
        row.refresh_from_db()
        self.assertIsNone(row.slug)
        self.assertEqual(
            list(MenuItem.objects.order_by('pk').values_list('pk', 'order')),
            [(pk, order) for pk, _parent, _title, order, _url, _slug in once],
        )

        links._remove_links(MenuItem)
        self.assertEqual(
            list(MenuItem.objects.order_by('pk').values_list(
                'pk', 'parent_id', 'title', 'order', 'url_name', 'slug',
            )),
            before,
        )

    def test_failure_rolls_back_earlier_inserts(self):
        nodes = self._tree()
        MenuItem.objects.filter(parent=nodes['real'], title='Калькуляторсуз').delete()
        before = MenuItem.objects.count()
        with self.assertRaises(links.MenuPathError):
            links._add_links(MenuItem)
        self.assertEqual(MenuItem.objects.count(), before)
        self.assertFalse(
            MenuItem.objects.filter(url_name__in=[spec['url_name'] for spec in links.LINKS]).exists()
        )

    def test_ambiguous_root_does_not_attach_anywhere(self):
        _node('Сандар', order=0)
        _node('Сандар', order=1)
        with self.assertRaises(links.MenuPathError):
            links._add_links(MenuItem)
        self.assertFalse(MenuItem.objects.filter(url_name='on_kozonoktuu_ramka').exists())

    def test_existing_row_under_the_wrong_parent_is_moved(self):
        nodes = self._tree()
        stray_parent = nodes['decoy_def'].parent
        stray = _node(
            'Башка аталыш',
            stray_parent,
            order=3,
            url_name='on_kozonoktuu_ramka',
            slug='old-slug',
        )
        links._add_links(MenuItem)
        stray.refresh_from_db()
        self.assertEqual(stray.parent_id, nodes['butun'].pk)
        self.assertEqual(stray.title, 'Он көзөнөктүү рамка')
        self.assertIsNone(stray.slug)
        self.assertEqual(
            MenuItem.objects.filter(url_name='on_kozonoktuu_ramka').count(),
            1,
        )
        self.assertEqual(_titles(nodes['butun'])[0][0], 'Он көзөнөктүү рамка')
        self.assertEqual(_titles(nodes['butun'])[1][0], 'Сан курамы')
