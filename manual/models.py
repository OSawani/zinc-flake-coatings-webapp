from django.db import models
from django.urls import reverse
import bleach
from core.models import User


# Function to clean HTML content
def clean_html(html_content):
    """
    Cleans the given HTML content to allow only a specified set of tags and
    attributes.

    Args:
        html_content (str): The HTML content to clean.

    Returns:
        str: The cleaned HTML content.
    """
    allowed_tags = bleach.sanitizer.ALLOWED_TAGS + [
        'p', 'br', 'div', 'span', 'img', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'th', 'tr', 'td', 'table', 'thead', 'tbody', 'sup', 'sub', 'ul', 'ol',
        'section', 'sup', 'sub', 'hr', 'blockquote', 'pre', 'code', 'a', 'li',
        'caption', 'figure', 'figcaption', 'summary', 'details', 'article',
        'button',
    ]
    allowed_attrs = {
        '*': ['class', 'style', 'src', 'href', 'alt', 'srcset', 'sizes',
              'loading', 'accordion-button', 'type', 'data-bs-toggle',
              'data-bs-target', 'aria-expanded', 'aria-controls', 'id', ]
    }

    cleaned_content = bleach.clean(html_content, tags=allowed_tags,
                                   attributes=allowed_attrs)
    return cleaned_content


# Create your models here.
class Section(models.Model):
    """
    model: `Section`

    This model represents a section with a title, description, author,
    and timestamps.

    Attributes: title (str): The title of the section. description (str):
    The description of the section. author (User): The author of the
    section. created_at (datetime): The date and time when the section was
    created. updated_at (datetime): The date and time when the section was
    last updated. css_path (str): The path to the CSS file for the section.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey('core.User', on_delete=models.SET_NULL,
                               null=True, blank=True, related_name='sections')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    css_path = models.CharField(null=True, blank=True)

    def __str__(self):
        """
        Returns the string representation of the section, which is its title.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the absolute URL for the section detail view.

        Returns:
            str: The absolute URL for the section detail view.
        """
        return reverse('section_detail_accordion', args=[self.id])

    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]


class Subsection(models.Model):
    """
    model: `Subsection`

    This model represents a subsection within a section, with a possible
    parent subsection, author, title, content, and timestamps.

    Attributes: section (Section): The section to which this subsection
    belongs. parent (Subsection): The parent subsection of this subsection.
    author (User): The author of the subsection. title (str): The title of
    the subsection. content (str): The content of the subsection. created_at
    (datetime): The date and time when the subsection was created.
    updated_at (datetime): The date and time when the subsection was last
    updated.
    """
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
        """
        Cleans HTML content before saving the subsection.
        """
        self.content = clean_html(self.content)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns the string representation of the subsection, which is its
        title.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the absolute URL for the subsection detail view.

        Returns:
            str: The absolute URL for the subsection detail view.
        """
        return f"{self.section.get_absolute_url()}#subsection-{self.id}"

    class Meta:
        indexes = [
            models.Index(fields=['section']),
            models.Index(fields=['parent']),
            models.Index(fields=['title']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]


class ContentVersion(models.Model):
    """
    model: `ContentVersion`

    This model represents a version of content within a subsection,
    including the version number, content, author, and timestamps.

    Attributes: subsection (Subsection): The subsection to which this
    version belongs. section (Section): The section to which this version
    belongs. version_number (int): The version number of the content.
    content (str): The content of the version. author (User): The author of
    the content version. created_at (datetime): The date and time when the
    content version was created. updated_at (datetime): The date and time
    when the content version was last updated.
    """
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
        """
        Returns the string representation of the content version, including
        its version number and the title of the subsection.
        """
        return f'Version {self.version_number} of {self.subsection.title}'
