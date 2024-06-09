import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = None # Remove the username field.
    # Use email as the username field
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_approved = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Unique related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all '
                  'permissions granted to each of their groups.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    USERNAME_FIELD = 'email' # Use email as unique identifier
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def send_approval_email(self):
        subject = 'Account Approved'
        message = ('Your account has been approved. You can now log in and '
                   'start writing comments and adding content to your '
                   'favourites.')
        send_mail(
            subject,
            message,
            os.environ.get('EMAIL_HOST_USER'),
            [self.email])