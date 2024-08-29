from string import Template

from django import forms
from django.forms import FileInput

from screenshots.models import Screenshot
from django.utils.safestring import mark_safe

class ScreenshotForm(forms.ModelForm):
    class Meta:
        model = Screenshot
        fields = ('screenshot','title','description')
        widgets = {
            'screenshot': forms.FileInput,
            'title' : forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
