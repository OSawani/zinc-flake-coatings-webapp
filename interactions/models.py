from django.db import models
from core.models import User
from manual.models import Section, Subsection


# Create your models here.
class Comment(models.Model):
    """
    model: `Comment`

    This model represents a comment made by a user on a section or subsection,
    including the content, approval status, and timestamps.

    Attributes: user (User): The user who made the comment. section (
    Section): The section the comment is related to. subsection (
    Subsection): The subsection the comment is related to. content (str):
    The content of the comment. approved (bool): The approval status of the
    comment. created_at (datetime): The date and time when the comment was
    created. updated_at (datetime): The date and time when the comment was
    last updated.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE,
                                related_name='comments', null=True, blank=True)
    subsection = models.ForeignKey(Subsection, on_delete=models.CASCADE,
                                   related_name='comments',
                                   null=True, blank=True)
    content = models.TextField()
    approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns the string representation of the comment, indicating the
        user who made it and the section or subsection it is related to.
        """
        if self.section:
            return (f'Comment by {self.user.email}'
                    f' on section {self.section.title}')
        return (f'Comment by {self.user.email}'
                f' on {self.subsection.title}')

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]


class Favourite(models.Model):
    """
    model: `Favourite`

    This model represents a user's favourite section or subsection,
    including timestamps.

    Attributes: user (User): The user who favourited the section or
    subsection. section (Section): The section that was favourited.
    subsection (Subsection): The subsection that was favourited. created_at
    (datetime): The date and time when the favourite was created. updated_at
    (datetime): The date and time when the favourite was last updated.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favourites')
    section = models.ForeignKey(Section, null=True, blank=True,
                                on_delete=models.CASCADE,
                                related_name='favourites')
    subsection = models.ForeignKey(Subsection, null=True, blank=True,
                                   on_delete=models.CASCADE,
                                   related_name='favourites')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns the string representation of the favourite, indicating the
        user and the favourited section or subsection.
        """
        if self.subsection:
            return (f'{self.user.email} favourited subsection: '
                    f'{self.subsection.title}')
        elif self.section:
            return (f'{self.user.email} favourited section:'
                    f' {self.section.title}')


class Notification(models.Model):
    """
    model: `Notification`

    This model represents a notification sent to a user, including the type,
    message, send status, and timestamps.

    Attributes: user (User): The user who receives the notification. type (
    str): The type of notification. message (str): The message content of
    the notification. sent (bool): The send status of the notification.
    created_at (datetime): The date and time when the notification was
    created. updated_at (datetime): The date and time when the notification
    was last updated.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='notifications')
    type = models.CharField(max_length=100)
    message = models.TextField()
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns the string representation of the notification, indicating
        the user who receives it.
        """
        return f'Notification for {self.user.email}'
