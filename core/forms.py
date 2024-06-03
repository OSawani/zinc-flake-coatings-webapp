from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Company


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        required=True,
        empty_label='Select a company'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2',
                  'company']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        # Set the username to the email (Email is unique)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
