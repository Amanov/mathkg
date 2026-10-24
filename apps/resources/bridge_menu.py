"""Insert the bridge pages into the existing area menu.

Additive and idempotent. Existing items are not renamed or deleted.
Missing parents are created so a fresh database still has somewhere to
hang the new links; on the live menu those parents are already there.
"""

from django.db.models import F, Max, Min


def apply_bridge_menu(MenuItem):
    """Return titles that were created on this call."""
    created = []

    def get_or_create(parent, title, url_name=''):
        item = MenuItem.objects.filter(title=title, parent=parent).first()
        if item is not None:
            if url_name and item.url_name != url_name:
                item.url_name = url_name
                item.save(update_fields=['url_name'])
            return item
        order = (MenuItem.objects.filter(parent=parent).aggregate(m=Max('order'))['m'] or 0) + 1
        item = MenuItem.objects.create(
            title=title,
            parent=parent,
            url_name=url_name or '',
            order=order,
        )
        created.append(title)
        return item

    def chain(titles):
        parent = None
        for title in titles:
            parent = get_or_create(parent, title)
        return parent

    def place_first(parent, item):
        others = MenuItem.objects.filter(parent=parent).exclude(pk=item.pk)
        min_order = others.aggregate(m=Min('order'))['m']
        if min_order is None or item.order < min_order:
            return
        if item.order == min_order:
            others.update(order=F('order') + 1)
            return
        MenuItem.objects.filter(parent=parent, order__gte=min_order).exclude(pk=item.pk).update(
            order=F('order') + 1,
        )
        item.order = min_order
        item.save(update_fields=['order'])

    def place_before(parent, item, before_title):
        sibling = MenuItem.objects.filter(parent=parent, title=before_title).exclude(pk=item.pk).first()
        if sibling is None or item.order < sibling.order:
            return
        old = sibling.order
        MenuItem.objects.filter(parent=parent, order__gte=old).exclude(pk=item.pk).update(
            order=F('order') + 1,
        )
        item.order = old
        item.save(update_fields=['order'])

    def place_after(parent, item, after_title):
        sibling = MenuItem.objects.filter(parent=parent, title=after_title).exclude(pk=item.pk).first()
        if sibling is None:
            return
        target = sibling.order + 1
        if item.order == target:
            return
        between = MenuItem.objects.filter(
            parent=parent, order__gt=sibling.order, order__lt=item.order,
        ).exclude(pk=item.pk)
        if item.order > sibling.order and not between.exists():
            return
        MenuItem.objects.filter(parent=parent, order__gte=target).exclude(pk=item.pk).update(
            order=F('order') + 1,
        )
        item.order = target
        item.save(update_fields=['order'])

    integers = chain(['Сандар', 'Бүтүн сандар'])
    sense = get_or_create(integers, 'Сан сезими')
    place_first(integers, sense)
    frame = get_or_create(sense, 'Он көзөнөктүү рамка', 'on_kozonoktuu_ramka')
    bonds = get_or_create(sense, 'Сан курамы', 'san_kuramy')
    place_first(sense, frame)
    place_after(sense, bonds, 'Он көзөнөктүү рамка')

    bars = get_or_create(integers, 'Тилке модели')
    place_after(integers, bars, 'Сан сезими')
    part = get_or_create(bars, 'Бөлүк–бүтүн тилке', 'bar_model_part_whole')
    comparison = get_or_create(bars, 'Салыштыруу тилкеси', 'bar_model_comparison')
    place_first(bars, part)
    place_after(bars, comparison, 'Бөлүк–бүтүн тилке')

    real_life = chain(['Сандар', 'Бүтүн сандар', 'Турмуштук маселелер'])
    words = get_or_create(real_life, 'Тексттик маселелер: тилке модели', 'word_problems_bar_model')
    place_after(real_life, words, 'Калькуляторсуз')

    ratio_change = chain(['Пропорция', 'Катыш', 'Өзгөртүп түзүү'])
    before = get_or_create(ratio_change, 'Мурун–кийин', 'before_after')
    place_after(ratio_change, before, 'Өзгөртүү')

    intro = chain(['Алгебра', 'Киришүү'])
    bar_x = get_or_create(intro, 'Тилкеден x ке', 'bar_to_x')
    place_first(intro, bar_x)

    linear = chain(['Алгебра', 'Теңдемелер: сызыктуу'])
    balance = get_or_create(linear, 'Тараза ыкмасы', 'balance_method')
    place_before(linear, balance, 'Белгисиз эки жагында')

    manipulation = chain(['Алгебра', 'Өзгөртүп түзүү'])
    tiles = get_or_create(manipulation, 'Алгебралык плиткалар', 'algebra_tiles')
    place_first(manipulation, tiles)

    get_or_create(None, 'Маселе чечүү', 'heuristics')
    return created
