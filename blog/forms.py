from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Comment, User


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")


class PostSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by title"
            }
        )
    )
