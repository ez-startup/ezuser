from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class UserManagerAdmin(UserAdmin):
    # Define the fields to display in the change list view
    list_display = ('username', 'first_name', 'last_name', 'nickname', 'gender', 'age',  'email', 'primary_phone', 'local_name', 'birthday', 'biography')

    # Define the fields to use for filtering in the right sidebar
    list_filter = ('groups', 'is_staff', 'is_superuser')

    # Customize the search fields
    search_fields = ('username', 'email', 'primary_phone', 'nickname', 'local_name')

    # Customize the fieldsets for the add and change forms
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Information', {'fields': ('first_name', 'last_name', 'age', 'nickname', 'local_name', 'gender', 'email', 'primary_phone', 'birthday', 'biography')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Customize the ordering of objects in the change list view
    ordering = ('-date_joined',)

admin.site.register(User, UserManagerAdmin)

