from django.contrib import admin

from .models import EventFeedback


@admin.register(EventFeedback)
class EventFeedbackAdmin(admin.ModelAdmin):
    list_display = ('event', 'get_student_name', 'rating', 'submitted_at')
    list_filter = ('rating', 'event', 'submitted_at')
    search_fields = ('student__email', 'student__first_name', 'student__last_name', 'event__title', 'comments')
    readonly_fields = ('submitted_at', 'updated_at')
    
    fieldsets = (
        ('Feedback Information', {
            'fields': ('event', 'student')
        }),
        ('Rating & Comments', {
            'fields': ('rating', 'comments')
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_student_name(self, obj):
        return obj.student.get_full_name()
    get_student_name.short_description = 'Student'
