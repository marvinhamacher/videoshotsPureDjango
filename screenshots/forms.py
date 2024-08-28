from django import forms

from screenshots.models import Screenshot


class ScreenshotForm(forms.ModelForm):
    class Meta:
        model = Screenshot
        fields = ('screenshot','title','description')
        widgets = {
            'screenshot': forms.ImageField(),
            'title' : forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
