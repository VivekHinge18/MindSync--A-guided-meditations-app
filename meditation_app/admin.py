from django.contrib import admin
from .models import MeditationSession, GuidedMeditation

admin.site.register(MeditationSession)
admin.site.register(GuidedMeditation)