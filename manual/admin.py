from django.contrib import admin
from django import forms
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.widgets import SummernoteWidget
from .models import Section, Subsection, ContentVersion


# Register your models here.
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'created_at', 'updated_at'
    )
    summernote_fields = ('description',)


# form for Subsection that uses SummernoteWidget for the content field
class SubsectionForm(forms.ModelForm):
    class Meta:
        model = Subsection
        fields = '__all__'
        widgets = {
             'content': SummernoteWidget(),
        }


@admin.register(Subsection)
class SubsectionAdmin(admin.ModelAdmin):
    form = SubsectionForm
    list_display = (
        'title',
        'section',
        'parent',
        'created_at', 'updated_at'
    )


@admin.register(ContentVersion)
class ContentVersionAdmin(admin.ModelAdmin):
    list_display = (
        'section',
        'subsection',
        'author',
        'version_number',
        'created_at', 'updated_at'
    )
