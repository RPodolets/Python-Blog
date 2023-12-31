from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import Textarea

from .models import Comment, User, Post, Tag


class UserForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        labels = ("",)
        widgets = {
            "content": Textarea(attrs={"rows": 5, "cols": 60}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].label = ""


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")


class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Post
        fields = ("title", "content", "tags")
        labels = ("",)
        widgets = {
            "content": Textarea(attrs={"rows": 8, "cols": 150}),
        }


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
