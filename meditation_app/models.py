from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class MeditationSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.PositiveIntegerField()  # Duration in minutes
    created_at = models.DateTimeField(auto_now_add=True)
    session_date = models.DateField(default=datetime.now().date)  # Corrected date default
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.user.username if self.user else 'Anonymous'}"

class GuidedMeditation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    audio_url = models.URLField(blank=True, null=True, help_text="Link to audio file")
    video_url = models.URLField(blank=True, null=True, help_text="Link to video file")

    def __str__(self):
        return self.title

class MeditationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meditation_type = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()  # Duration in seconds
    timestamp = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.user.username} - {self.meditation_type} ({self.duration // 60} min)"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    def __str__(self):
        return self.user.username
