from django.core.management.base import BaseCommand

from apps.resources.models import NewsPost

# Each entry's date reflects when that work actually shipped (real git
# history), written up as a teacher-facing summary rather than a dev
# commit log - internal-only work (deploy config, infra fixes) is left
# out on purpose since it's not something a site visitor needs to know.
NEWS_ITEMS = [
    {
        'published_date': '2026-09-26',
        'title': '"Сандар" менюсу иреттелди',
        'body': (
            '"Сандар" бөлүмүндөгү темалардын тизмеси иретке келтирилди: '
            'кайталанган жана туура эмес жайгашкан темалар оңдолуп, туура '
            'тартипте көрсөтүлдү. Мурда башка темалардын ичинде "жоголуп" '
            'калган сабактар (Төрт амал, Багытталган сандар, Кошуу сыяктуу) '
            'эми өз ордунда, тиешелүү темага байланды. Ошондой эле "Ондуктар" '
            'жана "Багытталган сандар" бөлүмдөрүнө бир нече жаңы кичи тема '
            'кошулду (Ондуктарды иреттөө, Ондуктун орун наркы, Багытталган '
            'сандарды иреттөө).'
        ),
    },
    {
        'published_date': '2026-09-26',
        'title': 'Азырынча материал жок бөлүмдөр көрсөтүлдү',
        'body': (
            'Мурда материал жүктөлбөгөн бөлүмдөр (мисалы, Геометрия, Ыктымалдуулук '
            'жана Дата темаларынын кээ бир бөлүмдөрү) бош барак катары көрүнчү. Эми '
            'ал жерлерде "Даярдалууда" деп белгиленген карталар менен кайсы '
            'материалдар (сабак презентациясы, иш баракча, көнүгүүлөр) даярдалып '
            'жатканы көрсөтүлөт.'
        ),
    },
    {
        'published_date': '2026-09-22',
        'title': 'Сайттын иконалору жана мобилдик көрүнүшү оңдолду',
        'body': (
            'Башкы менюдагы жана баракчалардагы иконалор туура көрсөтүлбөй калган '
            'эле - оңдолду. Ошону менен бирге, мобилдик телефондо меню баскычтары '
            'бирдей көрүнүш алды, ал эми темалардын аталыштары мурункудан алда канча '
            'окулмалуу болду.'
        ),
    },
    {
        'published_date': '2026-09-20',
        'title': 'Геометрия, Ыктымалдуулук жана Дата темалары кошулду',
        'body': (
            'Меню тизмегине үч жаңы негизги тема кошулду: Геометрия, Ыктымалдуулук '
            'жана Дата. Ар бир теманын ичинде ондогон бөлүм жана кичи бөлүм кыргыз '
            'тилинде уюштурулду.'
        ),
    },
    {
        'published_date': '2026-09-19',
        'title': 'Сайт MathKGZ деп аталды',
        'body': (
            'Платформа мурунку аталыштан MathKGZ деп кайра бренддештирилди - меню, '
            'баш аталыштар жана башка көрүнүктүү жерлерде жаңы аталыш колдонула баштады.'
        ),
    },
    {
        'published_date': '2026-09-18',
        'title': 'Башкы бетке жаңы сүрөттөр жана 3 айлык план кошулду',
        'body': (
            'Башкы беттеги бөлүмдөргө өзүнчө даярдалган жаңы иллюстрациялар кошулду. '
            'Жазылуу тандоолоруна 3 айлык план кошумча катары кошулду - мурункудай 6 '
            'айлык жана 1 жылдык пландар менен катар.'
        ),
    },
    {
        'published_date': '2026-09-17',
        'title': 'Биринчи бекер көнүгүү баракчасы жана QR аркылуу төлөм',
        'body': (
            'Кыргыз тилинде даярдалган биринчи бекер кайталоо баракчасы (Топтом 1-А) '
            'жарыяланды. Жазылууну QR код аркылуу төлөп ырастоо мүмкүнчүлүгү иштей '
            'баштады.'
        ),
    },
    {
        'published_date': '2026-09-16',
        'title': 'Сайт толугу менен кыргыз тилине которулду',
        'body': (
            'Интерфейстеги калган англис тилдеги жазуулар кыргыз тилине которулду. '
            'Ошону менен бирге сайттын коопсуздугу жана туруктуулугу боюнча бир катар '
            'жакшыртуулар жасалды.'
        ),
    },
]


class Command(BaseCommand):
    help = (
        "Seeds the launch-history NewsPost entries (real dated milestones from this "
        "project's own history, summarized for site visitors). Idempotent - matches "
        "existing rows by (title, published_date), safe to re-run. Pass --undo to "
        "remove exactly these entries."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--undo', action='store_true',
            help="Remove the seeded news entries instead of adding them.",
        )

    def handle(self, *args, **options):
        if options['undo']:
            self.undo()
        else:
            self.apply()

    def apply(self):
        for item in NEWS_ITEMS:
            post, created = NewsPost.objects.get_or_create(
                title=item['title'],
                published_date=item['published_date'],
                defaults={'body': item['body']},
            )
            verb = 'Created' if created else 'Already exists'
            self.stdout.write(f"{verb}: {post.published_date} - {post.title}")
        self.stdout.write(self.style.SUCCESS('Done.'))

    def undo(self):
        for item in NEWS_ITEMS:
            deleted, _ = NewsPost.objects.filter(
                title=item['title'], published_date=item['published_date'],
            ).delete()
            if deleted:
                self.stdout.write(f"Removed: {item['published_date']} - {item['title']}")
        self.stdout.write(self.style.SUCCESS('Undo complete.'))
