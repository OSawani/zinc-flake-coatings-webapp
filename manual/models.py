from django.db import models
from django.urls import reverse
from django_summernote.fields import SummernoteTextField
from core.models import User
import bleach


# Function to clean HTML content
def clean_html(html_content):
    allowed_tags = bleach.sanitizer.ALLOWED_TAGS + [
        'p', 'br', 'div', 'span', 'img', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'th', 'tr', 'td', 'table', 'thead', 'tbody', 'sup', 'sub', 'ul', 'ol',
    ]
    allowed_attrs = {
        '*': ['class', 'style', 'src', 'href', 'alt']
    }
    cleaned_content = bleach.clean(html_content, tags=allowed_tags,
                                   attributes=allowed_attrs)
    return cleaned_content


# Create your models here.
class Section(models.Model):
    title = models.CharField(max_length=255)
    description = SummernoteTextField(null=True, blank=True)
    author = models.ForeignKey('core.User', on_delete=models.SET_NULL,
                               null=True, blank=True, related_name='sections')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('section_detail', args=[self.id])


class Subsection(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE,
                                related_name='sub_sections')
    parent = models.ForeignKey('self', null=True, blank=True,
                               on_delete=models.CASCADE,
                               related_name='sub_sections')
    author = models.ForeignKey('core.User', on_delete=models.SET_NULL,
                               null=True, blank=True,
                               related_name='sub_sections')
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Clean HTML content before saving
        self.content = clean_html(self.content)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('subsection_detail', args=[self.id])


class ContentVersion(models.Model):
    subsection = models.ForeignKey(Subsection, on_delete=models.CASCADE,
                                   related_name='versions')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=True,
                                null=True, related_name='versions')
    version_number = models.IntegerField()
    content = models.TextField()
    author = models.ForeignKey('core.User', on_delete=models.SET_NULL,
                               null=True, blank=True,
                               related_name='published_versions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Version {self.version_number} of {self.subsection.title}'
