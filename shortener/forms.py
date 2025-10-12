from django import forms
from django.contrib.auth.models import User
from .models import ShortURL

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
        model = User
        fields = ("username", "email")

    def clean(self):
        cleaned = super().clean()
        pw = cleaned.get("password")
        pw2 = cleaned.get("password2")
        if pw and pw2 and pw != pw2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned
    
class ShortURLForm(forms.ModelForm):
    class Meta:
        model = ShortURL
        fields = ["original_url",]
        widgets = {
            "original_url": forms.URLInput(attrs={"placeholder": "https://example.com/very/long/url"})

        }