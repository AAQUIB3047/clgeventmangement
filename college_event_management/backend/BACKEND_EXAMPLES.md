# 🔧 Backend Examples & Best Practices

## Overview

This document provides examples and best practices for building Django REST APIs in the College Event Management system.

---

## 📁 Backend Structure

```
backend/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── event_management/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── users/                      # User management app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
├── events/                     # Events app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── registrations/              # Registrations app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── ...
├── attendance/                 # Attendance tracking
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── ...
└── reports/                    # Analytics & reports
    ├── models.py
    ├── views.py
    └── ...
```

---

## 📊 Database Models

### Users App Models

**Location:** `users/models.py`

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom User model with branch and Google OAuth support"""

    BRANCHES = [
        ('CSE', 'Computer Science'),
        ('ECE', 'Electronics'),
        ('ME', 'Mechanical'),
        ('CE', 'Civil'),
        ('EE', 'Electrical'),
        ('BIOTECH', 'Biotechnology'),
        ('OTHER', 'Other'),
    ]

    branch = models.CharField(max_length=20, choices=BRANCHES, null=True)
    google_id = models.CharField(max_length=100, unique=True, null=True)
    is_google_user = models.BooleanField(default=False)
    profile_picture = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class StudentEnrollment(models.Model):
    """Track student enrollments for attendance"""

    BRANCHES = [
        ('CSE', 'Computer Science'),
        ('ECE', 'Electronics'),
        ('ME', 'Mechanical'),
        ('CE', 'Civil'),
        ('EE', 'Electrical'),
        ('BIOTECH', 'Biotechnology'),
        ('OTHER', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='enrollment')
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    branch = models.CharField(max_length=20, choices=BRANCHES)
    roll_number = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['branch', 'full_name']
        verbose_name_plural = "Student Enrollments"

    def __str__(self):
        return f"{self.full_name} - {self.branch}"
```

---

## 🔗 Serializers

**Location:** `users/serializers.py`

```python
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import StudentEnrollment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Basic user serialization"""

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'branch',
                  'is_google_user', 'profile_picture', 'created_at']
        read_only_fields = ['id', 'created_at']


class GoogleAuthSerializer(serializers.Serializer):
    """Handle Google OAuth login"""

    token = serializers.CharField()
    branch = serializers.ChoiceField(
        choices=[
            ('CSE', 'Computer Science'),
            ('ECE', 'Electronics'),
            ('ME', 'Mechanical'),
            ('CE', 'Civil'),
            ('EE', 'Electrical'),
            ('BIOTECH', 'Biotechnology'),
            ('OTHER', 'Other'),
        ]
    )

    def validate_token(self, value):
        # Token validation logic
        if not value:
            raise serializers.ValidationError("Token is required")
        return value

    def create(self, validated_data):
        token = validated_data['token']
        branch = validated_data['branch']

        # Parse JWT and create/update user
        user_data = parse_jwt(token)

        user, created = User.objects.get_or_create(
            email=user_data['email'],
            defaults={
                'first_name': user_data.get('given_name', ''),
                'last_name': user_data.get('family_name', ''),
                'branch': branch,
                'google_id': user_data['sub'],
                'is_google_user': True,
                'profile_picture': user_data.get('picture'),
                'username': user_data['email'].split('@')[0]
            }
        )

        if not created:
            user.branch = branch
            user.save()

        return user


class StudentEnrollmentSerializer(serializers.ModelSerializer):
    """Serialize student enrollment data"""

    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = StudentEnrollment
        fields = ['id', 'user', 'email', 'full_name', 'branch',
                  'roll_number', 'user_email', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
```

---

## 🎯 Views & ViewSets

**Location:** `users/views.py`

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, GoogleAuthSerializer, StudentEnrollmentSerializer
from .models import StudentEnrollment

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """User management endpoints"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def google_login(self, request):
        """Google OAuth login endpoint"""

        serializer = GoogleAuthSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            # Create/update StudentEnrollment
            StudentEnrollment.objects.get_or_create(
                email=user.email,
                defaults={
                    'user': user,
                    'full_name': f"{user.first_name} {user.last_name}",
                    'branch': user.branch,
                }
            )

            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get current user profile"""

        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated, IsAdminUser])
    def enrollments(self, request):
        """Get all student enrollments (admin only)"""

        branch = request.query_params.get('branch')

        enrollments = StudentEnrollment.objects.all()
        if branch:
            enrollments = enrollments.filter(branch=branch)

        serializer = StudentEnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
```

---

## 🛣️ URL Routing

**Location:** `users/urls.py`

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

# Accessible at:
# POST   /api/users/google_login/
# GET    /api/users/profile/
# GET    /api/users/enrollments/ (admin only)
# GET    /api/users/ (list all users, admin only)
# POST   /api/users/ (create user, admin only)
# GET    /api/users/{id}/ (get user detail)
# PUT    /api/users/{id}/ (update user)
# DELETE /api/users/{id}/ (delete user, admin only)
```

---

## 👨‍💼 Admin Configuration

**Location:** `users/admin.py`

```python
from django.contrib import admin
from .models import User, StudentEnrollment

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Custom admin for User model"""

    list_display = ['email', 'first_name', 'last_name', 'branch',
                    'is_google_user', 'is_staff', 'created_at']
    list_filter = ['branch', 'is_google_user', 'is_staff', 'created_at']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-created_at']

    fieldsets = (
        ('Personal Info', {
            'fields': ('email', 'first_name', 'last_name', 'profile_picture')
        }),
        ('College Info', {
            'fields': ('branch',)
        }),
        ('Google OAuth', {
            'fields': ('google_id', 'is_google_user'),
            'classes': ('collapse',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')
        }),
        ('Timestamps', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['last_login', 'date_joined', 'created_at']


@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(admin.ModelAdmin):
    """Admin for StudentEnrollment model"""

    list_display = ['full_name', 'email', 'branch', 'roll_number', 'created_at']
    list_filter = ['branch', 'created_at']
    search_fields = ['email', 'full_name', 'roll_number']
    ordering = ['branch', 'full_name']

    fieldsets = (
        ('User Link', {
            'fields': ('user',)
        }),
        ('Personal Information', {
            'fields': ('full_name', 'email', 'roll_number')
        }),
        ('Branch Information', {
            'fields': ('branch',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at', 'updated_at']
```

---

## 🔐 Permissions & Authentication

```python
from rest_framework.permissions import BasePermission, IsAuthenticated

class IsAdmin(BasePermission):
    """Check if user is admin"""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsOwner(BasePermission):
    """Check if user is owner of object"""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


# Usage in views
class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]
```

---

## 🚀 API Response Examples

### Google Login

**Request:**

```bash
POST /api/users/google_login/
Content-Type: application/json

{
  "token": "eyJhbGc...",
  "branch": "CSE"
}
```

**Response (Success):**

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@gmail.com",
    "first_name": "John",
    "last_name": "Doe",
    "branch": "CSE",
    "is_google_user": true,
    "profile_picture": "https://lh3.googleusercontent.com/...",
    "created_at": "2025-01-15T10:30:00Z"
  }
}
```

### Get Enrollments (Admin)

**Request:**

```bash
GET /api/users/enrollments/?branch=CSE
Authorization: Bearer <access_token>
```

**Response:**

```json
[
  {
    "id": 1,
    "user": 1,
    "email": "student@gmail.com",
    "full_name": "John Doe",
    "branch": "CSE",
    "roll_number": "CSE-001",
    "user_email": "student@gmail.com",
    "created_at": "2025-01-15T10:30:00Z",
    "updated_at": "2025-01-15T10:30:00Z"
  }
]
```

---

## 📝 Best Practices

### 1. Model Definition

```python
# ✅ Good
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    capacity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Events"

    def __str__(self):
        return self.title

# ❌ Bad
class Event(models.Model):
    title = models.CharField(max_length=100)  # Too short
    # No timestamps
    # No ordering
```

### 2. Serializer Validation

```python
# ✅ Good
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'date', 'capacity']

    def validate_capacity(self, value):
        if value < 1:
            raise serializers.ValidationError("Capacity must be positive")
        return value

    def validate(self, data):
        if data['date'] < timezone.now():
            raise serializers.ValidationError("Date must be in future")
        return data

# ❌ Bad
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'  # Exposes everything
```

### 3. Permission Checking

```python
# ✅ Good
class EventViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

# ❌ Bad
class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser()]  # Too strict for all actions
```

### 4. Query Optimization

```python
# ✅ Good
class EventViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Event.objects.select_related('organizer').prefetch_related('attendees')

# ❌ Bad
def get_queryset(self):
    return Event.objects.all()  # N+1 query problem
```

---

## ✅ Deployment Checklist

- [ ] `DEBUG = False` in production settings
- [ ] `ALLOWED_HOSTS` configured properly
- [ ] Database migrations applied
- [ ] Static files collected
- [ ] Environment variables set (.env)
- [ ] CORS headers configured
- [ ] SSL/TLS enabled
- [ ] Rate limiting configured
- [ ] Logging configured
- [ ] Error monitoring (Sentry) setup

---

## 📚 References

- **Django Docs:** https://docs.djangoproject.com
- **DRF Docs:** https://www.django-rest-framework.org
- **JWT Auth:** https://django-rest-framework-simplejwt.readthedocs.io
- **Google OAuth:** https://developers.google.com/identity/protocols/oauth2
