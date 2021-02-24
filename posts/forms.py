from django import forms
from django.forms import Textarea

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')

        widgets = {"text": Textarea(attrs={"placeholder":
                                           "Введите текст записи",
                                           })}
