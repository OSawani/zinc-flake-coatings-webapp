from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Company


# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at', 'user_count']
    search_fields = ['name']

    def user_count(self, obj):
        return obj.employees.count()
    user_count.short_description = 'Number of Employees'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'first_name', 'last_name', 'company',
                    'is_approved']
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ['company', 'is_approved']
    ordering = ['company']
    actions = ['approve_users', 'reject_users']

    # Remove username field and use email as the unique identifier
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'company')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions')
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Approval', {'fields': ('is_approved',)}),
    )

    def approve_users(self, request, queryset):
        queryset.update(is_approved=True)
        for user in queryset:
            user.send_approval_email()

    approve_users.short_description = "Approve selected users"

    def reject_users(self, request, queryset):
        queryset.update(is_approved=False)

    reject_users.short_description = "Reject selected users"
