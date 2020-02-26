from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Score

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['score', 'musical_tests']
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn_primary'))

class AuthFormWithSubmit(AuthenticationForm):
    def __init__(self, request, *args, **kwargs):
        super(AuthFormWithSubmit, self).__init__(*args, **kwargs)
        self.request = request
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn_primary'))

class PasswordChangeFormWithSubmit(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeFormWithSubmit, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn_primary'))

class PwdResetFormWithSubmit(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PwdResetFormWithSubmit, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn_primary'))