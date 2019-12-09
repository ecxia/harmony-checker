from django import forms
from django.contrib.auth.models import User

from .models import Score


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['score', 'tests']

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
