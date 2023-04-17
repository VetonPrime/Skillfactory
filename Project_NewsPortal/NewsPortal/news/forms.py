from django import forms
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from .models import Post
from django.contrib.auth.models import Group


class NewForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'heading',
            'category',
            'author',
            'text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        heading = cleaned_data.get("heading")
        text = cleaned_data.get("text")

        if heading == text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
