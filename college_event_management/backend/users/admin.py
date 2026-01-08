from django.contrib import admin

from .models import AuditLog, Department, Faculty, Student, User


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name', 'department_code', 'head_of_department')
    search_fields = ('department_name', 'department_code')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'department', 'is_active')
    list_filter = ('role', 'branch', 'department', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name', 'username')
    readonly_fields = ('google_id', 'date_joined', 'last_login', 'created_at')
    
    fieldsets = (
        ('Account Information', {
            'fields': ('username', 'email', 'first_name', 'last_name', 'password')
        }),
        ('Google Auth', {
            'fields': ('is_google_user', 'google_id', 'profile_picture'),
            'classes': ('collapse',)
        }),
        ('Profile Information', {
            'fields': ('role', 'department', 'branch', 'phone_number')
        }),
        ('Permissions & Status', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Timestamps', {
            'fields': ('date_joined', 'last_login', 'created_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'get_full_name', 'department', 'year', 'created_at')
    list_filter = ('department', 'year', 'created_at')
    search_fields = ('roll_number', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Student Information', {
            'fields': ('user', 'roll_number', 'department', 'year')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Name'


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'get_full_name', 'designation', 'department', 'created_at')
    list_filter = ('department', 'designation', 'created_at')
    search_fields = ('employee_id', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Faculty Information', {
            'fields': ('user', 'employee_id', 'designation', 'department')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Name'


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'admin', 'action_type', 'entity_type', 'entity_id')
    list_filter = ('action_type', 'entity_type', 'timestamp')
    search_fields = ('admin__email', 'entity_type')
    readonly_fields = ('timestamp', 'admin', 'action_type', 'entity_type', 'entity_id', 'description', 'ip_address')
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
