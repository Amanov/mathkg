from datetime import date

from django.core.management.base import BaseCommand

from apps.resources.models import NewsPost

NEWS_ITEMS = [
    {
        'published_date': date(2026, 9, 16),
        'title': 'Мобилдик менюдагы категориялар тегиздалды',
        'body': (
            'Телефондо сайтты ачканда категориялар менюсундагы баскычтардын '
            '(Сандар, Пропорция, Алгебра ж.б.) туурасы ар кандай болуп, '
            'тегиз эмес көрүнчү. Эми бардык баскычтар бирдей туурада, бир '
            'тизме түрүндө көрсөтүлөт.'
        ),
    },
    {
        'published_date': date(2026, 9, 17),
        'title': 'Иш баракчалардын аталыштары окулуучу болду',
        'body': (
            'Активдүүлүктөрдүн аталыштары ("Цифралык табышмак" сыяктуу) '
            'кичине экрандарда өтө эле кичине көрүнүп, окуу кыйын болчу. '
            'Эми аталыштардын өлчөмү экрандын өлчөмүнө жараша ыңгайлуу '
            'туураланат.'
        ),
    },
    {
        'published_date': date(2026, 9, 18),
        'title': 'Даяр иш барактар бөлүмү толукталды',
        'body': (
            '"Даяр иш барактар" бөлүмүнө жаңы темалар жана деңгээлдер '
            'боюнча кошумча материалдар кошулду.'
        ),
    },
    {
        'published_date': date(2026, 9, 19),
        'title': 'Каттоо жана арыз берүү процесси жакшыртылды',
        'body': (
            'Мугалимдер үчүн каттоо жана жазылуу арызын жиберүү формасы '
            'жөнөкөйлөтүлдү, ката билдирүүлөр так жана түшүнүктүү болду.'
        ),
    },
    {
        'published_date': date(2026, 9, 21),
        'title': 'Жаңы SVG сүрөттөр башкы бетке кошулду',
        'body': (
            'Башкы беттеги темалык категорияларга (Сандар, Алгебра, '
            'Геометрия ж.б.) атайын иштелип чыккан сүрөттөр кошулуп, '
            'баракча визуалдык жактан жаңыртылды.'
        ),
    },
    {
        'published_date': date(2026, 9, 22),
        'title': 'Жаңылыктар жана "MathKGZ жөнүндө" барактары ачылды',
        'body': (
            'Платформага болгон өзгөрүүлөрдү ушул жерден таба аласыз. '
            'Ошондой эле MathKGZ жөнүндө жалпы маалымат камтылган "Жөнүндө" '
            'барагы кошулду.'
        ),
    },
]


class Command(BaseCommand):
    help = 'Seed initial launch news posts (idempotent). Use --undo to remove them.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--undo',
            action='store_true',
            help='Remove exactly the news posts this command creates.',
        )

    def handle(self, *args, **options):
        if options['undo']:
            titles = [item['title'] for item in NEWS_ITEMS]
            deleted, _ = NewsPost.objects.filter(title__in=titles).delete()
            self.stdout.write(self.style.SUCCESS(f'Removed {deleted} news post(s).'))
            return

        created_count = 0
        for item in NEWS_ITEMS:
            _, created = NewsPost.objects.get_or_create(
                title=item['title'],
                published_date=item['published_date'],
                defaults={'body': item['body']},
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Created {created_count} news post(s), {len(NEWS_ITEMS) - created_count} already existed.'
        ))
