from django.contrib import admin

from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'get_student_name', 'status', 'payment_status', 'attended', 'registration_time')
    list_filter = ('status', 'payment_status', 'attended', 'registration_time', 'event')
    search_fields = ('student__email', 'student__first_name', 'student__last_name', 'event__title')
    readonly_fields = ('registration_time', 'updated_at')
    
    fieldsets = (
        ('Registration Information', {
            'fields': ('event', 'student')
        }),
        ('Status', {
            'fields': ('status', 'attended')
        }),
        ('Payment', {
            'fields': ('payment_status', 'transaction_id')
        }),
        ('Timestamps', {
            'fields': ('registration_time', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_student_name(self, obj):
        return obj.student.get_full_name()
    get_student_name.short_description = 'Student'
