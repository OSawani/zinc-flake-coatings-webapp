from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Company


# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name']


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'first_name', 'last_name', 'company',
                    'is_approved']
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ['company', 'is_approved']

