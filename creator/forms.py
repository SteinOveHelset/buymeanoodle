from django.forms import ModelForm

from .models import Creator


class CreatorForm(ModelForm):
    class Meta:
        model = Creator
        fields = ('title', 'description', 'image',)