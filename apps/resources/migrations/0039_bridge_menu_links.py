"""Nine links in the menu that is already there.

Adds one MenuItem per bridge page below, under the section named by
``path``. «Маселе чечүү ыкмалары» (heuristics) is not a menu row; that
page stays as it is.

Parents are found by walking titles from the root. Each step must match
exactly one row, so a repeated title such as «Кошуу» or «Киришүү» is not
attached to the wrong section. A database with no menu roots (the test
database) is left unchanged.

``order`` is a positive integer, so a new row cannot sit between two
adjacent values without moving the later siblings of that parent up by
one. The same increment is what reverse undoes. Rows outside that parent
are not rewritten. A second run sees the row already in place and does
not move anyone again.
"""

from django.db import migrations, transaction
from django.db.models import F


class MenuPathError(RuntimeError):
    """A title path or sibling anchor was missing or not unique."""


LINKS = (
    {
        'title': 'Он көзөнөктүү рамка',
        'url_name': 'on_kozonoktuu_ramka',
        'path': ('Сандар', 'Бүтүн сандар'),
        'place': 'first',
        'before': 'Бүтүн сандардын орун наркы жана иреттөө',
    },
    {
        'title': 'Сан курамы',
        'url_name': 'san_kuramy',
        'path': ('Сандар', 'Бүтүн сандар'),
        'place': 'after',
        'after_url': 'on_kozonoktuu_ramka',
        'before': 'Бүтүн сандардын орун наркы жана иреттөө',
    },
    {
        'title': 'Бөлүк–бүтүн тилке',
        'url_name': 'bar_model_part_whole',
        'path': ('Сандар', 'Бүтүн сандар', 'Эсептөөлөр: 1 жана 2 орундук'),
        'place': 'first',
        'before': 'Кошуу',
    },
    {
        'title': 'Салыштыруу тилкеси',
        'url_name': 'bar_model_comparison',
        'path': ('Сандар', 'Бүтүн сандар', 'Эсептөөлөр: 1 жана 2 орундук'),
        'place': 'after',
        'after_url': 'bar_model_part_whole',
        'before': 'Кошуу',
    },
    {
        'title': 'Тилке модели',
        'url_name': 'word_problems_bar_model',
        'path': ('Сандар', 'Бүтүн сандар', 'Турмуштук маселелер'),
        'place': 'last',
        'after': 'Калькуляторсуз',
    },
    {
        'title': 'Мурун–кийин',
        'url_name': 'before_after',
        'path': ('Пропорция', 'Катыш', 'Өзгөртүп түзүү'),
        'place': 'last',
        'after': 'Өзгөртүү',
    },
    {
        'title': 'Тилкеден x ке',
        'url_name': 'bar_to_x',
        'path': ('Алгебра', 'Киришүү'),
        'place': 'first',
        'before': 'Аныктамалар',
    },
    {
        'title': 'Тараза ыкмасы',
        'url_name': 'balance_method',
        'path': ('Алгебра', 'Теңдемелер: сызыктуу'),
        'place': 'between',
        'after': 'Түзүү',
        'before': 'Белгисиз бир жагында: калькулятор менен',
    },
    {
        'title': 'Алгебралык плиткалар',
        'url_name': 'algebra_tiles',
        'path': ('Алгебра', 'Өзгөртүп түзүү'),
        'place': 'first',
        'before': 'Белгилөө',
    },
)


def _children(MenuItem, parent, exclude_pk=None):
    rows = MenuItem.objects.filter(parent=parent)
    if exclude_pk is not None:
        rows = rows.exclude(pk=exclude_pk)
    return rows


def _require_sibling(rows, title, context):
    matches = rows.filter(title=title)
    count = matches.count()
    if count != 1:
        raise MenuPathError(f'{context}: {title!r} matched {count} siblings')
    return matches.get()


def _resolve_parent(MenuItem, path):
    parent = None
    walked = []
    for title in path:
        walked.append(title)
        matches = MenuItem.objects.filter(parent=parent, title=title)
        count = matches.count()
        if count != 1:
            raise MenuPathError(
                f'{title!r} along {" › ".join(walked)} matched {count} rows'
            )
        parent = matches.get()
    return parent


def _existing(MenuItem, url_name):
    matches = MenuItem.objects.filter(url_name=url_name)
    count = matches.count()
    if count > 1:
        raise MenuPathError(f'{url_name!r} matched {count} menu rows')
    return matches.first()


def _already_placed(MenuItem, item, parent, spec):
    if item.parent_id != parent.pk:
        return False
    others = _children(MenuItem, parent, exclude_pk=item.pk)
    place = spec['place']
    if place == 'first':
        anchor = others.filter(title=spec['before'])
        if anchor.count() != 1 or item.order >= anchor.get().order:
            return False
        return not others.filter(order__lte=item.order).exists()
    if place == 'after':
        predecessor = MenuItem.objects.filter(
            parent=parent, url_name=spec['after_url'],
        ).first()
        anchor = others.filter(title=spec['before'])
        if predecessor is None or predecessor.pk == item.pk or anchor.count() != 1:
            return False
        if not (predecessor.order < item.order < anchor.get().order):
            return False
        earlier = list(others.filter(order__lt=item.order).values_list('pk', flat=True))
        return earlier == [predecessor.pk]
    if place == 'last':
        anchor = others.filter(title=spec['after'])
        if anchor.count() != 1 or item.order <= anchor.get().order:
            return False
        return not others.filter(order__gte=item.order).exists()
    if place == 'between':
        left = others.filter(title=spec['after'])
        right = others.filter(title=spec['before'])
        if left.count() != 1 or right.count() != 1:
            return False
        return left.get().order < item.order < right.get().order
    raise MenuPathError(f"unknown place {place!r}")


def _clear_extra_fields(item, spec):
    changed = []
    if item.title != spec['title']:
        item.title = spec['title']
        changed.append('title')
    for field in ('slug', 'topic', 'subtopic', 'subsubtopic'):
        if getattr(item, field):
            setattr(item, field, None)
            changed.append(field)
    if changed:
        item.save(update_fields=changed)


def _slot(MenuItem, parent, spec, exclude_pk):
    others = _children(MenuItem, parent, exclude_pk=exclude_pk)
    context = spec['url_name']
    place = spec['place']
    if place == 'first':
        _require_sibling(others, spec['before'], context)
        orders = list(others.values_list('order', flat=True))
        if not orders:
            raise MenuPathError(f'{context}: section has no sibling to precede')
        return min(orders)
    if place == 'after':
        predecessors = MenuItem.objects.filter(parent=parent, url_name=spec['after_url'])
        if exclude_pk is not None:
            predecessors = predecessors.exclude(pk=exclude_pk)
        if predecessors.count() != 1:
            raise MenuPathError(
                f'{context}: {spec["after_url"]!r} matched {predecessors.count()} siblings'
            )
        predecessor = predecessors.get()
        anchor = _require_sibling(others, spec['before'], context)
        if anchor.order <= predecessor.order:
            raise MenuPathError(
                f'{context}: {spec["before"]!r} is not after {spec["after_url"]}'
            )
        return predecessor.order + 1
    if place == 'last':
        anchor = _require_sibling(others, spec['after'], context)
        orders = list(others.values_list('order', flat=True))
        slot = max(orders) + 1
        if anchor.order >= slot:
            raise MenuPathError(f'{context}: {spec["after"]!r} is not before the end')
        return slot
    if place == 'between':
        left = _require_sibling(others, spec['after'], context)
        right = _require_sibling(others, spec['before'], context)
        if left.order >= right.order:
            raise MenuPathError(
                f'{context}: {spec["after"]!r} is not before {spec["before"]!r}'
            )
        return right.order
    raise MenuPathError(f"unknown place {place!r}")


def _place(MenuItem, spec):
    parent = _resolve_parent(MenuItem, spec['path'])
    existing = _existing(MenuItem, spec['url_name'])
    if existing is not None and _already_placed(MenuItem, existing, parent, spec):
        _clear_extra_fields(existing, spec)
        return
    exclude_pk = existing.pk if existing is not None else None
    slot = _slot(MenuItem, parent, spec, exclude_pk)
    _children(MenuItem, parent, exclude_pk=exclude_pk).filter(order__gte=slot).update(
        order=F('order') + 1
    )
    if existing is None:
        MenuItem.objects.create(
            title=spec['title'],
            parent=parent,
            url_name=spec['url_name'],
            order=slot,
            slug=None,
            topic=None,
            subtopic=None,
            subsubtopic=None,
        )
        return
    existing.parent = parent
    existing.title = spec['title']
    existing.url_name = spec['url_name']
    existing.order = slot
    existing.slug = None
    existing.topic = None
    existing.subtopic = None
    existing.subsubtopic = None
    existing.save()


def _add_links(MenuItem):
    if not MenuItem.objects.filter(parent__isnull=True).exists():
        return
    with transaction.atomic():
        for spec in LINKS:
            _place(MenuItem, spec)


def _remove_links(MenuItem):
    with transaction.atomic():
        for spec in reversed(LINKS):
            matches = MenuItem.objects.filter(url_name=spec['url_name'])
            count = matches.count()
            if count == 0:
                continue
            if count > 1:
                raise MenuPathError(f'{spec["url_name"]!r} matched {count} menu rows')
            item = matches.get()
            parent_id = item.parent_id
            order = item.order
            item.delete()
            MenuItem.objects.filter(parent_id=parent_id, order__gt=order).update(
                order=F('order') - 1
            )


def add_menu_links(apps, schema_editor):
    _add_links(apps.get_model('personal', 'MenuItem'))


def remove_menu_links(apps, schema_editor):
    _remove_links(apps.get_model('personal', 'MenuItem'))


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0038_four_packs'),
    ]

    operations = [
        migrations.RunPython(add_menu_links, remove_menu_links),
    ]
