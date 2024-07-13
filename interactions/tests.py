from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from interactions.models import Comment
from interactions.forms import CommentForm
from manual.models import Section
from allauth.account.models import EmailAddress
from core.models import Company

User = get_user_model()

class TestCommentForm(TestCase):

    def test_form_is_valid(self):
        form_data = {'content': 'This is a comment'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid(), msg="Form is invalid")

    def test_form_is_invalid(self):
        form_data = {'content': ''}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid(), msg="Form is valid")

class TestInteractionsViews(TestCase):

    def setUp(self):
        self.company = Company.objects.create(name="Test Company")
        self.user = User.objects.create(
            email="testuser@example.com",
            password="Test@12345",  # Password meeting the criteria
            first_name="John",
            last_name="Doe",
            company=self.company,
            is_approved=True
        )
        self.user.set_password("Test@12345")  # Ensure the password is hashed properly
        self.user.save()
        self.client.login(email='testuser@example.com', password='Test@12345')
        self.section = Section.objects.create(title="Test Section", author=self.user)

        # Mock email verification
        EmailAddress.objects.create(user=self.user, email=self.user.email, verified=True, primary=True)

    def test_add_comment_to_section(self):
        response = self.client.post(reverse('add_comment_to_section', args=[self.section.id]), {
            'content': 'This is a test comment.'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Comment.objects.filter(content='This is a test comment.').exists())

    def test_edit_comment(self):
        # First, add a comment to edit
        comment = Comment.objects.create(user=self.user, section=self.section, content='Original content')

        response = self.client.post(reverse('edit_section_comment', args=[comment.id]), {
            'content': 'Updated content'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Updated content')

    def test_delete_comment(self):
        # First, add a comment to delete
        comment = Comment.objects.create(user=self.user, section=self.section, content='Content to delete')

        response = self.client.post(reverse('delete_section_comment', args=[comment.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())