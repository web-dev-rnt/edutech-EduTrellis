# live_class/models.py
from django.db import models
from django.utils.text import slugify
from video_courses.models import Category


class LiveClassCourse(models.Model):
    name = models.CharField(max_length=220, unique=True)
    language = models.CharField(max_length=64)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_free = models.BooleanField(default=False, help_text="Check if this is a free course")
    banner_image_desktop = models.ImageField(upload_to='live_courses/banner_desktop/', blank=True, null=True)
    banner_image_mobile = models.ImageField(upload_to='live_courses/banner_mobile/', blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    about = models.TextField(blank=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name='live_class_courses',
        verbose_name='Category'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def category_name(self):
        """Return category name for display purposes"""
        return self.category.name if self.category else "No Category"
    
    @property
    def display_price(self):
        """Return display price or 'Free' text"""
        if self.is_free:
            return "Free"
        return f"₹{self.current_price}"
    
    @property
    def course_type(self):
        """Return course type for filtering"""
        return "Free" if self.is_free else "Paid"


class LiveClassSession(models.Model):
    course = models.ForeignKey(
        LiveClassCourse, 
        on_delete=models.CASCADE, 
        related_name='sessions'
    )
    class_name = models.CharField(max_length=200)
    subject = models.CharField(max_length=200, blank=True, null=True)
    scheduled_datetime = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    max_participants = models.PositiveIntegerField(default=100)
    is_free = models.BooleanField(default=False, help_text="Override course pricing for this session")
    enable_auto_recording = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['scheduled_datetime']

    def __str__(self):
        return f"{self.course.name} - {self.class_name}"

    @property
    def ends_at(self):
        from datetime import timedelta
        return self.scheduled_datetime + timedelta(minutes=self.duration_minutes)


class LiveClassRecording(models.Model):
    """A teacher's recording of a live class, streamed from their browser into Dropbox while the class runs."""

    STATUS_CHOICES = [
        ('recording', 'Recording'),
        ('ready', 'Ready'),
        ('failed', 'Failed'),
    ]
    STORAGE_CHOICES = [
        ('dropbox', 'Dropbox'),
        ('local', 'Server disk'),
    ]

    session = models.ForeignKey(LiveClassSession, on_delete=models.CASCADE, related_name='recordings')
    title = models.CharField(max_length=200, blank=True)
    file_name = models.CharField(max_length=500, blank=True, help_text='Path inside the storage (Dropbox: under /elibrary/)')
    storage = models.CharField(max_length=10, choices=STORAGE_CHOICES, default='dropbox')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='recording')
    mime_type = models.CharField(max_length=80, default='video/webm')
    size_bytes = models.BigIntegerField(default=0)
    duration_seconds = models.PositiveIntegerField(default=0)
    upload_session_id = models.CharField(max_length=255, blank=True)
    is_published = models.BooleanField(default=True, help_text='Show to enrolled students')
    started_by = models.ForeignKey('base.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title or f"{self.session} recording"

    @property
    def size_mb(self):
        return round(self.size_bytes / (1024 * 1024), 1)

    @property
    def duration_display(self):
        minutes, seconds = divmod(self.duration_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes}:{seconds:02d}"
