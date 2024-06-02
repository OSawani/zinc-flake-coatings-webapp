from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Section, Subsection, ContentVersion


# Register your models here.
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')


@admin.register(Subsection)
class SubsectionAdmin(SummernoteModelAdmin):
    list_display = ('title', 'section', 'parent', 'created_at', 'updated_at')
    summernote_fields = ('content',)


@admin.register(ContentVersion)
class ContentVersionAdmin(admin.ModelAdmin):
    list_display = ('section', 'subsection', 'author', 'version_number', 'created_at', 'updated_at')
