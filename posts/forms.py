from django import forms
from django.forms import Textarea

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')

        widgets = {"text": Textarea(attrs={"placeholder":
                                           "Введите текст записи",
                                           })}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

        widgets = {"text": Textarea(attrs={"placeholder":
                                           "Ваш комментарий очень важен для "
                                           "нас",
                                           })}
