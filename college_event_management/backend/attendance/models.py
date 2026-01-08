from django.contrib.auth import get_user_model
from django.db import models
from events.models import Event

User = get_user_model()


class Attendance(models.Model):
    VERIFICATION_METHODS = [
        ('qr_code', 'QR Code'),
        ('manual', 'Manual Entry'),
        ('biometric', 'Biometric'),
        ('rfid', 'RFID Card'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendance_records')
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, related_name='attendance_records')
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    verification_method = models.CharField(max_length=20, choices=VERIFICATION_METHODS, default='manual')

    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
        unique_together = ('event', 'student')
        ordering = ['-check_in_time']

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.event.title}"
