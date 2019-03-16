from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm


class ProfileForm(forms.ModelForm):
    nickname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control profile-input'}), required=False)
    about = forms.CharField(widget=forms.Textarea(attrs={'class':'noresize form-control profile-input', 'rows':4}), required=False)
    image = forms.FileField(widget=forms.FileInput(attrs={'class':'custom-file-input profile-input'}), required=False)

    class Meta:
        model = Profile
        fields = ['nickname','about','image',]


class BootstrapUserCreationForm(UserCreationForm):
    error_css_class = 'is-invalid'


class BootstrapPasswordChangeForm(PasswordChangeForm):
    error_css_class = 'is-invalid'
