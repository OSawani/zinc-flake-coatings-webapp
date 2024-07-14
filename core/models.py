import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail


# Create your models here.
class Company(models.Model):
    """
    model: `Company`

    This model represents a company with a unique name.

    Attributes: name (str): The name of the company. created_at (datetime):
    The date and time when the company was created. updated_at (datetime):
    The date and time when the company was last updated.
    """
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns the string representation of the company, which is its name.
        """
        return self.name


class User(AbstractUser):
    """
    model: `User`

    This model represents a user which extends the default Django
    `AbstractUser` model, using email as the username field and including
    additional fields like first name, last name, approval status,
    and a foreign key to a `Company`.

    Attributes:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The unique email address of the user.
        is_approved (bool): The approval status of the user.
        company (Company): The company to which the user belongs.
        created_at (datetime): The date and time when the user was created.
        updated_at (datetime): The date and time when the user was last updated
        groups (ManyToManyField): The groups this user belongs to.
        user_permissions (ManyToManyField): Specific permissions for this user.
    """
    username = None
    # Remove the username field.
    # Use email as the username field
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_approved = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True,
                                blank=True, related_name='employees')
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

    USERNAME_FIELD = 'email'
    # Use email as unique identifier
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        """
        Returns the string representation of the user, which is their email.
        """
        return self.email

    def send_approval_email(self):
        """
        Sends an approval email to the user notifying them that their
        account has been approved.
        """
        subject = 'Konto Freigegeben'
        message = ('Ihr Konto wurde genehmigt. Sie können sich nun anmelden '
                   'und anfangen, Kommentare zu schreiben und Inhalte zu '
                   'Ihren Favoriten hinzuzufügen.')
        send_mail(
            subject,
            message,
            os.environ.get('EMAIL_HOST_USER'),
            [self.email])
