#!/usr/bin/env python
import os
import sys
import django

# Add the backend directory to the path
sys.path.insert(0, r'C:\Users\admin\Desktop\ONE MORE\college_event_management\backend')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile

email = 'qureshiaaquib1304@gmail.com'
password = 'aaquib1304'

try:
    # Try to get existing user
    user = User.objects.get(email=email)
    print(f"User with email {email} already exists")
except User.DoesNotExist:
    # Create new user
    user = User.objects.create_user(
        username=email.split('@')[0],
        email=email,
        password=password,
        is_staff=True,
        is_superuser=True
    )
    print(f"Created new superuser: {email}")

# Update existing user to be superuser/staff
user.is_staff = True
user.is_superuser = True
user.set_password(password)
user.save()

# Update UserProfile to make them admin
try:
    profile = UserProfile.objects.get(user=user)
except UserProfile.DoesNotExist:
    profile = UserProfile.objects.create(user=user)

profile.role = 'admin'
profile.is_active = True
profile.save()

print(f"✅ User {email} set as admin with password: {password}")
print(f"✅ is_staff: {user.is_staff}")
print(f"✅ is_superuser: {user.is_superuser}")
print(f"✅ UserProfile role: {profile.role}")
