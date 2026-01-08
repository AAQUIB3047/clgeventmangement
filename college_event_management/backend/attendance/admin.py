from django.contrib import admin

from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('event', 'get_student_name', 'check_in_time', 'check_out_time', 'verification_method')
    list_filter = ('verification_method', 'event', 'check_in_time')
    search_fields = ('student__email', 'student__first_name', 'student__last_name', 'event__title')
    readonly_fields = ('check_in_time', 'check_out_time')
    
    fieldsets = (
        ('Attendance Information', {
            'fields': ('event', 'student')
        }),
        ('Check Times', {
            'fields': ('check_in_time', 'check_out_time')
        }),
        ('Verification', {
            'fields': ('verification_method',)
        }),
    )
    
    def get_student_name(self, obj):
        return obj.student.get_full_name()
    get_student_name.short_description = 'Student'
