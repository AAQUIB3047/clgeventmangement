from django.contrib import admin

from .models import StudentEnrollment, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'branch', 'is_google_user', 'is_active')
    list_filter = ('role', 'branch', 'is_google_user', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name', 'username')
    readonly_fields = ('google_id', 'date_joined', 'last_login')
    
    fieldsets = (
        ('Account Information', {
            'fields': ('username', 'email', 'first_name', 'last_name', 'password')
        }),
        ('Google Auth', {
            'fields': ('is_google_user', 'google_id', 'profile_picture'),
            'classes': ('collapse',)
        }),
        ('Profile Information', {
            'fields': ('role', 'branch', 'phone_number', 'department')
        }),
        ('Permissions & Status', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Timestamps', {
            'fields': ('date_joined', 'last_login'),
            'classes': ('collapse',)
        }),
    )


@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'branch', 'roll_number', 'created_at')
    list_filter = ('branch', 'created_at')
    search_fields = ('email', 'full_name', 'roll_number')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Student Information', {
            'fields': ('user', 'email', 'full_name', 'branch', 'roll_number')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
