from django import forms
from .models import MeditationSession, UserProfile

class MeditationSessionForm(forms.ModelForm):
    class Meta:
        model = MeditationSession
        fields = ['title', 'description', 'duration']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']