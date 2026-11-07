import os
from io import BytesIO
from logging import getLogger

from PIL import Image as PILImage

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.conf import settings
from django.urls import reverse, NoReverseMatch

logger = getLogger(__name__)

# =====================================================

# TOPICS

# =====================================================

class Topic(models.Model):
    title = models.CharField(max_length=200)

    title_ru = models.CharField(
        'Орусча аталыш',
        max_length=200,
        blank=True,
        help_text='Издөө үчүн гана. Барактын өзү кыргызча бойдон калат.',
    )

    slug = models.SlugField(unique=True)

    icon = models.CharField(
        max_length=50,
        blank=True
    )

    order = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('topic_detail', args=[self.slug])

    class Meta:
        ordering = ['order']


# =====================================================

# CHOICES

# =====================================================

LEARNING_GOALS = [


    ('presentation', 'Сабактын презентациясы'),

    ('patterns', 'Мыйзамченемдүүлүктөр'),

    ('visuals', 'Визуалдык түшүнүү'),

    ('discussion', 'Математикалык талкуу'),

    ('discovery', 'Изилдөө жана ачылыш'),

    ('fluency', 'Машыгуу жана флюенттүүлүк'),

    ('retrieval', 'Кайталоо жана эстеп калуу'),

    ('problem_solving', 'Маселе чыгаруу'),

    ('modelling', 'Турмушта колдонуу'),

    ('proof', 'Далилдөө жана негиздөө'),

    ('games', 'Оюндар'),


    ]

ACTIVITY_TYPES = [


('lesson', 'Lesson'),

('abc', 'ABC'),
('show_me', 'Show Me'),

('answer_grid', 'Answer Grid'),
('answer_maze', 'Answer Maze'),
('create_question', 'Create Question'),
('digit_puzzle', 'Digit Puzzle'),
('four_in_row', 'Four In Row'),
('link', 'Link'),
('true_false_maze', 'True False Maze'),
('worded', 'Worded'),

('card_match', 'Card Match'),
('card_sort', 'Card Sort'),
('messenger', 'Messenger'),
('relay_race', 'Relay Race'),
('treasure_trail', 'Treasure Trail'),

('three_stars', '3 Stars'),
('bingo', 'Bingo'),
('blockbusters', 'Blockbusters'),
('car_race', 'Car Race'),
('noughts_crosses', 'Noughts & Crosses'),
('penalty_shootout', 'Penalty Shootout'),
('shootout', 'Shootout'),
('splat', 'Splat'),
('yes_no_maybe', 'Yes No Maybe'),


]

DIFFICULTY_CHOICES = [


('easy', 'Easy'),
('medium', 'Medium'),
('hard', 'Hard'),
('challenge', 'Challenge'),


]

# =====================================================

# RESOURCES

# =====================================================

class Resource(models.Model):
    CATEGORY_CHOICES = [
        ('presentation', 'Презентация'),
        ('worksheet', 'Иш барак'),
        ('activity', 'Мугалим жетектеген ишмердик'),
        ]

    topic = models.ForeignKey(
        Topic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resources'
    )
    subtopic = models.ForeignKey("Subtopic",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resources"
    )

    subsubtopic = models.ForeignKey("SubSubtopic",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resources"
    )

    learning_goal = models.CharField(
        max_length=50,
        choices=LEARNING_GOALS,
        blank=True
    )

    activity_type = models.CharField(
        max_length=50,
        choices=ACTIVITY_TYPES,
        blank=True
    )

    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='medium'
    )

    

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    file = models.FileField(
        upload_to='resources/files/'
    )

    image = models.ImageField(
        upload_to='resources/images/',
        blank=True,
        null=True
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    is_active = models.BooleanField(
        default=True
    )

    download_count = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def increment_download(self):
        self.download_count += 1
        self.save(update_fields=['download_count'])

    def save(self, *args, **kwargs):
        if self.image and not self.image.name.lower().endswith('.webp'):
            converted = self._image_as_webp()
            if converted is not None:
                self.image = converted
        super().save(*args, **kwargs)

    def _image_as_webp(self):
        """Re-encode the currently-assigned image upload as lossless WebP
        (same pixels, usually 40-60% smaller than the PNG/JPEG it replaces -
        see docs/deployment-notes.md). Returns None (leaving the original
        upload untouched) if the file can't be read as an image, rather
        than raising - a bad upload should fail loudly elsewhere (or just
        not get a thumbnail), not block saving the whole Resource."""
        try:
            self.image.seek(0)
            pil_image = PILImage.open(self.image)
            pil_image.load()
        except Exception as e:
            logger.error('Could not read image for WebP conversion: %s', e)
            return None

        buffer = BytesIO()
        try:
            pil_image.save(buffer, format='WEBP', lossless=True)
        except Exception as e:
            logger.error('Could not encode image as WebP: %s', e)
            return None

        new_name = os.path.splitext(self.image.name)[0] + '.webp'
        return ContentFile(buffer.getvalue(), name=new_name)

    def clean(self):
        if self.subtopic_id and not self.topic_id:
            raise ValidationError("Pick a Topic before picking a Subtopic.")
        if self.subtopic_id and self.topic_id and self.subtopic.topic_id != self.topic_id:
            raise ValidationError("That Subtopic doesn't belong to the selected Topic.")
        if self.subsubtopic_id and not self.subtopic_id:
            raise ValidationError("Pick a Subtopic before picking a Sub-subtopic.")
        if self.subsubtopic_id and self.subtopic_id and self.subsubtopic.subtopic_id != self.subtopic_id:
            raise ValidationError("That Sub-subtopic doesn't belong to the selected Subtopic.")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Resource'
        verbose_name_plural = 'Resources'


class Subtopic(models.Model):

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='subtopics'
    )

    title = models.CharField(max_length=200)

    title_ru = models.CharField(
        'Орусча аталыш',
        max_length=200,
        blank=True,
        help_text='Издөө үчүн гана. Барактын өзү кыргызча бойдон калат.',
    )

    slug = models.SlugField()

    order = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('subtopic_detail', args=[self.topic.slug, self.slug])

    class Meta:
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(
                fields=['topic', 'slug'],
                name='personal_subtopic_topic_slug_uniq',
            ),
        ]

# add this to apps/resources/models.py after Subtopic

class SubSubtopic(models.Model):
    subtopic = models.ForeignKey(
        Subtopic,
        on_delete=models.CASCADE,
        related_name='subsubtopics'
    )
    title = models.CharField(max_length=200)
    title_ru = models.CharField(
        'Орусча аталыш',
        max_length=200,
        blank=True,
        help_text='Издөө үчүн гана. Барактын өзү кыргызча бойдон калат.',
    )
    slug = models.SlugField()
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'subsubtopic_detail',
            args=[self.subtopic.topic.slug, self.subtopic.slug, self.slug],
        )

    class Meta:
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(
                fields=['subtopic', 'slug'],
                name='personal_subsubtopic_subtopic_slug_uniq',
            ),
        ]

# =====================================================

# DOWNLOAD ANALYTICS

# =====================================================

class ResourceDownload(models.Model):
    resource = models.ForeignKey(
    Resource,
    on_delete=models.CASCADE,
    related_name='downloads'
)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    downloaded_at = models.DateTimeField(
        auto_now_add=True
    )

    user_agent = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ['-downloaded_at']
        verbose_name = 'Download Log'
        verbose_name_plural = 'Download Logs'

    def __str__(self):
        user_str = self.user.username if self.user else self.ip_address
        return f"{user_str} - {self.resource.title}"


class PageFreeDownload(models.Model):
    """The one file a topic page gives away.

    Filled with a random choice the first time that page is built, then
    kept. Staff can point `resource` at a different file and leave
    `pinned` on so the next visit does not replace their choice.
    """

    page_key = models.CharField(max_length=80, unique=True)
    resource = models.ForeignKey(
        Resource,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='free_on_pages',
    )
    pinned = models.BooleanField(
        default=False,
        help_text='Admin override. Leave this on to keep the file chosen above.',
    )

    class Meta:
        verbose_name = 'Free download'
        verbose_name_plural = 'Free downloads'

    def __str__(self):
        return f'{self.page_key}: {self.resource or "—"}'


# =====================================================

# SITE TRAFFIC ANALYTICS

# =====================================================

class SiteVisit(models.Model):
    session_key = models.CharField(
        max_length=40,
        blank=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    path = models.CharField(
        max_length=255
    )

    visited_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-visited_at']
        verbose_name = 'Site Visit'
        verbose_name_plural = 'Site Visits'

    def __str__(self):
        who = self.user.username if self.user else (self.session_key[:8] or self.ip_address)
        return f"{who} - {self.path}"


class ButtonClick(models.Model):
    label = models.CharField(
        max_length=120
    )

    path = models.CharField(
        max_length=255,
        blank=True
    )

    session_key = models.CharField(
        max_length=40,
        blank=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    clicked_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-clicked_at']
        verbose_name = 'Button Click'
        verbose_name_plural = 'Button Clicks'

    def __str__(self):
        return f"{self.label} - {self.clicked_at:%Y-%m-%d %H:%M}"


class SearchQuery(models.Model):
    query = models.CharField(
        max_length=255
    )

    results_count = models.PositiveIntegerField(
        default=0
    )

    session_key = models.CharField(
        max_length=40,
        blank=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    searched_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-searched_at']
        verbose_name = 'Search Query'
        verbose_name_plural = 'Search Queries'

    def __str__(self):
        return f"{self.query} ({self.results_count}) - {self.searched_at:%Y-%m-%d %H:%M}"


class LoginEvent(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='login_events'
    )

    session_key = models.CharField(
        max_length=40,
        blank=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    logged_in_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-logged_in_at']
        verbose_name = 'Login Event'
        verbose_name_plural = 'Login Events'

    def __str__(self):
        return f"{self.user.username} - {self.logged_in_at:%Y-%m-%d %H:%M}"


class AnalyticsWindow(models.Model):
    """Singleton cutoff for the staff analytics dashboard.

    When stats_since is set, the dashboard counts events at or after
    that instant. Clearing it shows all-time totals again. SiteVisit,
    ButtonClick, SearchQuery, LoginEvent, ResourceDownload, and
    PageReaction rows are never deleted by this.
    """

    stats_since = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Analytics window'
        verbose_name_plural = 'Analytics window'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        if self.stats_since:
            return f'since {self.stats_since:%Y-%m-%d %H:%M}'
        return 'all time'

    @classmethod
    def stored_since(cls):
        row = cls.objects.filter(pk=1).only('stats_since').first()
        return row.stats_since if row else None

    @classmethod
    def set_since(cls, value):
        cls.objects.update_or_create(pk=1, defaults={'stats_since': value})


# for data driven menu

class MenuItem(models.Model):
    title = models.CharField(max_length=200)

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children'
    )

    url_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text=(
            "Only for a fixed, argument-less page (e.g. 'directed_numbers'). "
            "To link to a topic/subtopic/sub-subtopic page, use the Topic/"
            "Subtopic/Sub-subtopic fields below instead - they take "
            "priority over this one when set."
        ),
    )


    slug = models.SlugField(
    blank=True,
    null=True
    )

    # Linking straight to a browsable content page needs up to three
    # slugs (topic/subtopic/subsubtopic_detail all take slug arguments),
    # which a single free-text field can't hold safely - these give staff
    # a plain dropdown picker instead of hand-typed, typo-prone slugs.
    topic = models.ForeignKey(
        'Topic',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='menu_items',
        help_text="Links to this topic's page. Leave Subtopic/Sub-subtopic blank for a topic-level link.",
    )

    subtopic = models.ForeignKey(
        'Subtopic',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='menu_items',
        help_text="Must belong to the Topic selected above.",
    )

    subsubtopic = models.ForeignKey(
        'SubSubtopic',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='menu_items',
        help_text="Must belong to the Subtopic selected above.",
    )

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def clean(self):
        if self.subtopic_id and not self.topic_id:
            raise ValidationError("Pick a Topic before picking a Subtopic.")
        if self.subtopic_id and self.topic_id and self.subtopic.topic_id != self.topic_id:
            raise ValidationError("That Subtopic doesn't belong to the selected Topic.")
        if self.subsubtopic_id and not self.subtopic_id:
            raise ValidationError("Pick a Subtopic before picking a Sub-subtopic.")
        if self.subsubtopic_id and self.subtopic_id and self.subsubtopic.subtopic_id != self.subtopic_id:
            raise ValidationError("That Sub-subtopic doesn't belong to the selected Subtopic.")

    def get_resolved_url(self):
        """The URL for a topic/subtopic/sub-subtopic link, most specific
        first - or None if none of those three fields are set (in which
        case the template falls back to url_name)."""
        try:
            if self.subsubtopic_id:
                return reverse('subsubtopic_detail', args=[
                    self.topic.slug, self.subtopic.slug, self.subsubtopic.slug,
                ])
            if self.subtopic_id:
                return reverse('subtopic_detail', args=[self.topic.slug, self.subtopic.slug])
            if self.topic_id:
                return reverse('topic_detail', args=[self.topic.slug])
        except NoReverseMatch:
            return None
        return None


# =====================================================

# NEWS

# =====================================================

KYRGYZ_MONTHS = [
    'январь', 'февраль', 'март', 'апрель', 'май', 'июнь',
    'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь',
]


class NewsPost(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(
        help_text="Кыска түшүндүрмө - эмне өзгөрдү же кошулду.",
    )
    published_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_date', '-created_at']
        verbose_name = 'Жаңылык'
        verbose_name_plural = 'Жаңылыктар'

    def formatted_date(self):
        d = self.published_date
        return f"{d.day}-{KYRGYZ_MONTHS[d.month - 1]}, {d.year}-жыл"

    def __str__(self):
        return f"{self.published_date}: {self.title}"


# =====================================================

# PAGE REACTIONS AND WRITTEN FEEDBACK

# =====================================================

class PageReaction(models.Model):
    """One visitor's face for one page.

    A second tap from the same visitor and page is ignored. Counts for
    the admin list live on PageReactionCount, updated in the same save.
    """

    FACE_HAPPY = 'happy'
    FACE_OK = 'ok'
    FACE_SAD = 'sad'
    FACE_CHOICES = [
        (FACE_HAPPY, '😊 Жакты'),
        (FACE_OK, '😐 Жаман эмес'),
        (FACE_SAD, '🙁 Жаккан жок'),
    ]

    path = models.CharField(max_length=255, db_index=True)
    face = models.CharField(max_length=10, choices=FACE_CHOICES)
    # The topic page's own material (its title). Empty on pages that are
    # not a topic page, such as the home page.
    material = models.CharField(max_length=255, blank=True)
    topic = models.ForeignKey(
        Topic,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='page_reactions',
    )
    subtopic = models.ForeignKey(
        Subtopic,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='page_reactions',
    )
    subsubtopic = models.ForeignKey(
        SubSubtopic,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='page_reactions',
    )
    visitor_key = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Page reaction'
        verbose_name_plural = 'Page reactions'
        constraints = [
            models.UniqueConstraint(
                fields=['path', 'visitor_key'],
                name='personal_reaction_visitor_page_uniq',
            ),
        ]

    def __str__(self):
        return f'{self.get_face_display()} {self.path}'


class PageReactionCount(models.Model):
    """Per-page totals, so the admin list can be sorted by most 🙁."""

    path = models.CharField(max_length=255, unique=True)
    material = models.CharField(max_length=255, blank=True)
    happy_count = models.PositiveIntegerField('😊', default=0)
    ok_count = models.PositiveIntegerField('😐', default=0)
    sad_count = models.PositiveIntegerField('🙁', default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-sad_count', '-happy_count', 'path']
        verbose_name = 'Page reaction count'
        verbose_name_plural = 'Page reaction counts'

    def __str__(self):
        return self.material or self.path


class WrittenFeedback(models.Model):
    """A teacher's longer note from /pikir/.

    Nothing is shown on «Мугалимдердин пикирлери» until show_on_site is
    set in the admin. The public page never receives the email.
    """

    KIND_OPINION = 'pikir'
    KIND_SUGGESTION = 'sunush'
    KIND_PRAISE = 'maktoo'
    KIND_CHOICES = [
        (KIND_OPINION, 'Пикир'),
        (KIND_SUGGESTION, 'Сунуш'),
        (KIND_PRAISE, 'Мактоо'),
    ]

    kind = models.CharField('Type', max_length=16, choices=KIND_CHOICES)
    message = models.TextField()
    name = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    about_page = models.CharField('Page', max_length=255, blank=True)
    is_read = models.BooleanField('Read', default=False)
    show_on_site = models.BooleanField(
        'Show on site',
        default=False,
        help_text='Approved notes appear on «Мугалимдердин пикирлери».',
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Written feedback'
        verbose_name_plural = 'Written feedback'

    def __str__(self):
        return f'{self.get_kind_display()}: {self.message[:40]}'

    def public_name(self):
        name = (self.name or '').strip()
        return name or 'Мугалим'


# =====================================================

# QUESTION BANK AND GENERATED TESTS

# =====================================================

class Question(models.Model):
    """One item in the teacher test bank.

    Multiple choice uses the Cyrillic letters А Б В Г. Short answers and
    word problems leave options empty and store the expected answer as text.
    """

    TYPE_MULTIPLE_CHOICE = 'multiple_choice'
    TYPE_SHORT_ANSWER = 'short_answer'
    TYPE_WORD_PROBLEM = 'word_problem'
    TYPE_CHOICES = [
        (TYPE_MULTIPLE_CHOICE, 'Көп тандоо'),
        (TYPE_SHORT_ANSWER, 'Кыска жооп'),
        (TYPE_WORD_PROBLEM, 'Тексттик маселе'),
    ]

    FORMAT_CHOICE = 'choice'
    FORMAT_SHORT = 'short_response'
    FORMAT_EXTENDED = 'extended'
    FORMAT_CALCULATION = 'calculation'
    FORMAT_DIAGRAM = 'diagram'
    FORMAT_TRUE_FALSE = 'true_false'
    FORMAT_MATCHING = 'matching'
    FORMAT_FILL_BLANK = 'fill_blank'
    # Older rows used one «written» bucket. Migrations split it.
    FORMAT_WRITTEN = 'written'
    FORMAT_CHOICES = [
        (FORMAT_CHOICE, 'Тест (жооп тандоо)'),
        (FORMAT_SHORT, 'Кыска жооп'),
        (FORMAT_EXTENDED, 'Кеңири жооп (жазуу менен чыгаруу)'),
        (FORMAT_CALCULATION, 'Эсептөө'),
        (FORMAT_DIAGRAM, 'Сүрөт боюнча'),
        (FORMAT_TRUE_FALSE, 'Туура/туура эмес'),
        (FORMAT_MATCHING, 'Дал келтирүү'),
        (FORMAT_FILL_BLANK, 'Боштукту толтуруу'),
    ]
    OPEN_FORMATS = (
        FORMAT_SHORT, FORMAT_EXTENDED, FORMAT_CALCULATION, FORMAT_DIAGRAM,
        FORMAT_FILL_BLANK, FORMAT_WRITTEN,
    )

    DIFFICULTY_EASY = 'easy'
    DIFFICULTY_MEDIUM = 'medium'
    DIFFICULTY_HARD = 'hard'
    DIFFICULTY_VERY_HARD = 'very_hard'
    DIFFICULTY_CHOICES = [
        (DIFFICULTY_EASY, 'Жеңил'),
        (DIFFICULTY_MEDIUM, 'Орто'),
        (DIFFICULTY_HARD, 'Оор'),
        (DIFFICULTY_VERY_HARD, 'Өтө оор'),
    ]

    OPTION_LETTERS = ('А', 'Б', 'В', 'Г')
    GRADE_CHOICES = [(n, f'{n}-класс') for n in range(1, 12)]

    grade = models.PositiveSmallIntegerField('Класс', choices=GRADE_CHOICES)
    topic = models.ForeignKey(
        Topic,
        on_delete=models.PROTECT,
        related_name='questions',
        verbose_name='Тема',
    )
    difficulty = models.CharField(
        'Деңгээл',
        max_length=16,
        choices=DIFFICULTY_CHOICES,
    )
    question_format = models.CharField(
        'Суроонун түрү',
        max_length=32,
        choices=FORMAT_CHOICES,
        default=FORMAT_CHOICE,
    )
    question_type = models.CharField(
        'Түрү',
        max_length=32,
        choices=TYPE_CHOICES,
    )
    text = models.TextField('Суроо')
    options = models.JSONField(
        'Варианттар',
        default=dict,
        blank=True,
        help_text='Көп тандоо үчүн: {"А": "...", "Б": "...", "В": "...", "Г": "..."}.',
    )
    answer = models.CharField(
        'Жооп',
        max_length=255,
        help_text='Көп тандоодо А, Б, В же Г. Башка түрлөрдө кыска жооп.',
    )
    solution = models.TextField(
        'Чыгарылышы',
        blank=True,
        help_text='Жооп ачкычындагы кадамдар. Классикалык суроодо көрсөтүлөт.',
    )
    points = models.PositiveSmallIntegerField('Балл', default=1)
    estimated_minutes = models.PositiveSmallIntegerField(
        'Болжолдуу мүнөт',
        default=2,
        help_text='Бул суроого кете турган болжолдуу убакыт.',
    )
    is_published = models.BooleanField('Жарыяланган', default=True)
    is_sample = models.BooleanField(
        'Үлгү',
        default=False,
        help_text='Үлгү банк. Мугалимге үлгү экени көрүнөт.',
    )
    sample_key = models.CharField(
        max_length=64,
        unique=True,
        null=True,
        blank=True,
        help_text='Үлгү суроону кайра жүктөө үчүн туруктуу ачкыч.',
    )

    class Meta:
        ordering = ['grade', 'topic', 'difficulty', 'pk']
        verbose_name = 'Суроо'
        verbose_name_plural = 'Суроолор'
        indexes = [
            models.Index(fields=['grade', 'is_published']),
            models.Index(fields=['topic', 'grade', 'is_published']),
        ]

    def __str__(self):
        text = ' '.join(self.text.split())
        if len(text) > 60:
            text = text[:60] + '…'
        return f'{self.grade}-класс: {text}'

    def clean(self):
        super().clean()
        if self.grade not in dict(self.GRADE_CHOICES):
            raise ValidationError({'grade': 'Класс 1ден 11ге чейин болушу керек.'})
        if self.points < 1:
            raise ValidationError({'points': 'Балл кеминде 1 болушу керек.'})
        options = self.options or {}
        if not isinstance(options, dict):
            raise ValidationError({'options': 'Варианттар сөздүк түрүндө болушу керек.'})
        if self.question_format == self.FORMAT_MATCHING:
            left = options.get('left') or {}
            right = options.get('right') or {}
            if not isinstance(left, dict) or not isinstance(right, dict) or not left or not right:
                raise ValidationError({
                    'options': 'Дал келтирүү үчүн сол жана оң тилке керек.',
                })
            if not (self.answer or '').strip():
                raise ValidationError({'answer': 'Жоопту жазыңыз.'})
            return
        if self.question_format in (self.FORMAT_CHOICE, self.FORMAT_TRUE_FALSE):
            letters = self.OPTION_LETTERS if self.question_format == self.FORMAT_CHOICE else ('А', 'Б')
            missing = [
                letter for letter in letters
                if not str(options.get(letter, '')).strip()
            ]
            if missing:
                raise ValidationError({
                    'options': 'Керектүү тамгалар толтурулушу керек: ' + ', '.join(missing) + '.',
                })
            if (self.answer or '').strip() not in letters:
                raise ValidationError({'answer': 'Жооп көрсөтүлгөн тамгалардын бири болушу керек.'})
        elif not (self.answer or '').strip():
            raise ValidationError({'answer': 'Жоопту жазыңыз.'})


class GeneratedTest(models.Model):
    """One test a teacher generated. Counts toward the monthly limit."""

    TYPE_FORMATIVE = 'formative'
    TYPE_UNIT = 'unit'
    TYPE_QUARTER = 'quarter'
    TYPE_SUMMATIVE = 'summative'
    TYPE_CHOICES = [
        (TYPE_FORMATIVE, 'Калыптандыруучу'),
        (TYPE_UNIT, 'Бөлүм боюнча'),
        (TYPE_QUARTER, 'Чейрек'),
        (TYPE_SUMMATIVE, 'Жыйынтыктоочу'),
    ]

    MIX_EQUAL = 'teng'
    MIX_MOSTLY_EASY = 'kobuncho_jenil'
    MIX_MOSTLY_MEDIUM = 'kobuncho_orto'
    MIX_MOSTLY_HARD = 'kobuncho_oor'
    MIX_EASY = 'jenil'
    MIX_MEDIUM = 'orto'
    MIX_HARD = 'oor'
    MIX_CHOICES = [
        (MIX_EQUAL, 'Баары бирдей'),
        (MIX_MOSTLY_EASY, 'Көбүнчө жеңил'),
        (MIX_MOSTLY_MEDIUM, 'Көбүнчө орто'),
        (MIX_MOSTLY_HARD, 'Көбүнчө оор'),
        (MIX_EASY, 'Жеңил гана'),
        (MIX_MEDIUM, 'Орто гана'),
        (MIX_HARD, 'Оор гана'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='generated_tests',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    grade = models.PositiveSmallIntegerField()
    test_type = models.CharField(max_length=32, choices=TYPE_CHOICES)
    question_count = models.PositiveSmallIntegerField()
    variant_count = models.PositiveSmallIntegerField()
    difficulty_mix = models.CharField(max_length=32, choices=MIX_CHOICES, default=MIX_EQUAL)
    format_mode = models.CharField(max_length=16, default='mixed')
    extra_formats = models.JSONField(default=list, blank=True)
    formats = models.JSONField(default=list, blank=True)
    levels = models.JSONField(default=list, blank=True)
    duration_minutes = models.PositiveSmallIntegerField(default=45)
    show_timer = models.BooleanField(default=False)
    title = models.CharField(max_length=120, blank=True)
    payload = models.JSONField()
    topics = models.ManyToManyField(Topic, blank=True, related_name='generated_tests')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Түзүлгөн тест'
        verbose_name_plural = 'Түзүлгөн тесттер'
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f'{self.grade}-класс, {self.get_test_type_display()}'