from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('organizer', 'Organizer'),
        ('admin', 'Admin'),
    ]
    
    BRANCH_CHOICES = [
        ('cse', 'Computer Science & Engineering'),
        ('ece', 'Electronics & Communication'),
        ('eee', 'Electrical & Electronics'),
        ('me', 'Mechanical Engineering'),
        ('ce', 'Civil Engineering'),
        ('it', 'Information Technology'),
        ('other', 'Other'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    phone_number = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=100, blank=True)
    branch = models.CharField(max_length=20, choices=BRANCH_CHOICES, default='other', blank=True)
    google_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    is_google_user = models.BooleanField(default=False)
    profile_picture = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class StudentEnrollment(models.Model):
    """Store student email and branch information for attendance tracking"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='enrollment')
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    branch = models.CharField(max_length=20, choices=User.BRANCH_CHOICES)
    roll_number = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Student Enrollment'
        verbose_name_plural = 'Student Enrollments'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} ({self.email}) - {self.branch}"
