from django.db import models
from django.conf import settings

# =====================================================

# TOPICS

# =====================================================

class Topic(models.Model):
    title = models.CharField(max_length=200)

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

    ('problem_solving', 'Маселе чечүү'),

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
        ('presentation', 'Presentation'),
        ('worksheet', 'Worksheet'),
        ('activity', 'Activity'),
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

    slug = models.SlugField()

    order = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']

# add this to apps/resources/models.py after Subtopic

class SubSubtopic(models.Model):
    subtopic = models.ForeignKey(
        Subtopic,
        on_delete=models.CASCADE,
        related_name='subsubtopics'
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']

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
        null=True
    )
   

    slug = models.SlugField(
    blank=True,
    null=True
    )

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title