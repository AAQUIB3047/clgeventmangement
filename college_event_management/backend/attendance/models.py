from django.db import models
from registrations.models import Registration

class Attendance(models.Model):
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE, related_name='attendance')
    checked_in = models.BooleanField(default=False)
    check_in_time = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Attendance for {self.registration}"
