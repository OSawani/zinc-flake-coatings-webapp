from django import forms
from allauth.account.forms import SignupForm
from .models import User, Company


class CustomSignupForm(SignupForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        required=True,
        empty_label='Select a company'
    )

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.company = self.cleaned_data['company']
        user.save()
        return user
