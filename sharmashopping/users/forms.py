from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'type': 'text',
            'class': 'form-control border-0 p-4',
            'placeholder': 'Your name',
            'required': 'required',
        })
        self.fields["email"].widget.attrs.update({
            'type': 'text',
            'class': 'form-control border-0 p-4',
            'placeholder': 'Your email',
            'required': 'required',
        })
        self.fields["password1"].widget.attrs.update({
            'type': 'password',
            'class': 'form-control border-0 p-4',
            'placeholder': 'Password',
            'required': 'required',
        })
        self.fields["password2"].widget.attrs.update({
            'type': 'password',
            'class': 'form-control border-0 p-4',
            'placeholder': 're-enter Password',
            'required': 'required',
        })

        email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
