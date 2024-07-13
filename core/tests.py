from django.test import TestCase
from core.forms import CustomSignupForm
from core.models import Company


class TestCustomSignupForm(TestCase):

    def setUp(self):
        self.company = Company.objects.create(name="Test Company")

    def test_form_is_valid(self):
        form_data = {
            'email': 'testuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'company': self.company.id,
            'password1': 'qWSDe43-.,ss',
            'password2': 'qWSDe43-.,ss'
        }
        form = CustomSignupForm(data=form_data)
        self.assertTrue(form.is_valid(), msg="Form is invalid")

    def test_form_is_invalid(self):
        form_data = {
            'email': '',
            'first_name': 'John',
            'last_name': 'Doe',
            'company': self.company.id,
            'password1': 'qWSDe43-.,ss',
            'password2': 'qWSDe43-.,ss'
        }
        form = CustomSignupForm(data=form_data)
        self.assertFalse(form.is_valid(), msg="Form is valid")
