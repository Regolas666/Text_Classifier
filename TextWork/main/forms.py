from .models import Articles
from django.forms import ModelForm, TextInput, Textarea


class ArticlesForm(ModelForm):
    class Meta:  # доп. настройки
        model = Articles
        fields = ["tag", "title", "full_text"]
        widgets = {
            "tag": TextInput(attrs={
                'class': 'form_control',
                'placeholder': 'Введитие тег',
                'size': '95'
            }),
            "title": TextInput(attrs={
                'class': 'form_control',
                'placeholder': 'Введитие заголовок',
                'size': '95'
            }),
            "full_text": Textarea(attrs={
                'size': '95',
                'class': 'form_control',
                'placeholder': 'Введитие текст',
                'rows': '15',
                'cols': '98',
            }),
        }


class TextsFormSecond(ModelForm):
    class Meta:
        model = Articles
        fields = ["full_text"]
        widgets = {
            "full_text": Textarea(attrs={
                'size': '95',
                'class': 'form_control',
                'placeholder': 'Введитие текст',
                'rows': '15',
                'cols': '98',

            })
        }
