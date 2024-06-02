from django.db import models
from django_summernote.fields import SummernoteTextField


# Create your models here.
class Section(models.Model):
    title = models.CharField(max_length=255)
    description = SummernoteTextField
    author = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Subsection(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = SummernoteTextField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ContentVersion(models.Model):
    subsection = models.ForeignKey(Subsection, on_delete=models.CASCADE)
    version_number = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Version {self.version_number} of {self.subsection.title}'
