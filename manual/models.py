from django.db import models
from django.urls import reverse
from django_summernote.fields import SummernoteTextField
from core.models import User


# Create your models here.
class Section(models.Model):
    title = models.CharField(max_length=255)
    description = SummernoteTextField(null=True, blank=True)
    author = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='sections')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('section_detail', args=[self.id])


class Subsection(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='sub_sections')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='sub_sections')
    author = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='sub_sections')
    title = models.CharField(max_length=255)
    content = SummernoteTextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('subsection_detail', args=[self.id])


class ContentVersion(models.Model):
    subsection = models.ForeignKey(Subsection, on_delete=models.CASCADE, related_name='versions')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=True, null=True, related_name='versions')
    version_number = models.IntegerField()
    content = models.TextField()
    author = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='published_versions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Version {self.version_number} of {self.subsection.title}'
