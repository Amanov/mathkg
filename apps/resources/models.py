import random
import string

from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.urls import reverse, NoReverseMatch

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

# QUESTION BANK / ONLINE TESTS

# =====================================================

class Question(models.Model):
    QUESTION_TYPES = [
        ('mcq', 'Көп тандоолуу'),
        ('short', 'Кыска жооп'),
    ]

    CHOICE_LETTERS = [
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D'),
    ]

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='questions',
    )

    topic = models.ForeignKey(
        Topic, null=True, blank=True, on_delete=models.SET_NULL, related_name='questions',
    )
    subtopic = models.ForeignKey(
        Subtopic, null=True, blank=True, on_delete=models.SET_NULL, related_name='questions',
    )
    subsubtopic = models.ForeignKey(
        SubSubtopic, null=True, blank=True, on_delete=models.SET_NULL, related_name='questions',
    )

    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='mcq')
    text = models.TextField()
    image = models.ImageField(upload_to='questions/images/', blank=True, null=True)

    choice_a = models.CharField(max_length=255, blank=True)
    choice_b = models.CharField(max_length=255, blank=True)
    choice_c = models.CharField(max_length=255, blank=True)
    choice_d = models.CharField(max_length=255, blank=True)
    correct_choice = models.CharField(max_length=1, choices=CHOICE_LETTERS, blank=True)

    correct_answer_text = models.CharField(
        max_length=255, blank=True,
        help_text="'Кыска жооп' түрүндөгү суроолор автоматтык бааланбайт - бул мугалимге эталон жооп катары гана көрсөтүлөт.",
    )

    marks = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        if self.subtopic_id and not self.topic_id:
            raise ValidationError("Теманы тандабай туруп, бөлүмдү тандай албайсыз.")
        if self.subtopic_id and self.topic_id and self.subtopic.topic_id != self.topic_id:
            raise ValidationError("Тандалган бөлүм тандалган темага таандык эмес.")
        if self.subsubtopic_id and not self.subtopic_id:
            raise ValidationError("Бөлүмдү тандабай туруп, кичи бөлүмдү тандай албайсыз.")
        if self.subsubtopic_id and self.subtopic_id and self.subsubtopic.subtopic_id != self.subtopic_id:
            raise ValidationError("Тандалган кичи бөлүм тандалган бөлүмгө таандык эмес.")
        if self.question_type == 'mcq' and not self.correct_choice:
            raise ValidationError("Көп тандоолуу суроо үчүн туура жоопту (A/B/C/D) көрсөтүү керек.")

    def __str__(self):
        return self.text[:60]


class Exam(models.Model):
    title = models.CharField(max_length=255)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='exams',
    )

    questions = models.ManyToManyField(Question, through='ExamQuestion', related_name='exams')

    access_code = models.CharField(max_length=8, unique=True, blank=True)
    is_published = models.BooleanField(default=False)
    time_limit_minutes = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @staticmethod
    def _generate_access_code():
        alphabet = string.ascii_uppercase + string.digits
        while True:
            code = ''.join(random.choices(alphabet, k=6))
            if not Exam.objects.filter(access_code=code).exists():
                return code

    def save(self, *args, **kwargs):
        if not self.access_code:
            self.access_code = self._generate_access_code()
        super().save(*args, **kwargs)

    def total_marks(self):
        return sum(
            eq.question.marks
            for eq in self.examquestion_set.select_related('question')
        )

    def __str__(self):
        return self.title


class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ('exam', 'question')


class ExamAttempt(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts')
    student_name = models.CharField(max_length=150)
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    score = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.student_name} — {self.exam.title}"


class ExamAnswer(models.Model):
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.CharField(max_length=1, blank=True)
    answer_text = models.CharField(max_length=500, blank=True)
    is_correct = models.BooleanField(null=True)