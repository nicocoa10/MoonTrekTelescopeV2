from django import forms
from .models import MoonPost

class MoonPostForm(forms.ModelForm):
    class Meta:
        model = MoonPost
        fields= ('user_image',)
