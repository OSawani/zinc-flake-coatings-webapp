from django.db import models
from core.models import User
from manual.models import Section, Subsection


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subsection = models.ForeignKey(Subsection, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.user.email} on {self.subsection.title}'


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
    section = models.ForeignKey(Section, null=True, blank=True, on_delete=models.CASCADE, related_name='favourites')
    subsection = models.ForeignKey(Subsection, null=True, blank=True, on_delete=models.CASCADE, related_name='favourites')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.subsection:
            return f'{self.user.email} favourited subsection: {self.subsection.title}'
        elif self.section:
            return f'{self.user.email} favourited section: {self.section.title}'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=100)
    message = models.TextField()
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Notification for {self.user.email}'
