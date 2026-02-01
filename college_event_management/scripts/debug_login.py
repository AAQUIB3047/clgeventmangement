import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'college_event_management', 'backend'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from django.contrib.auth import authenticate
from users.models import User

# Check the user
try:
    user = User.objects.get(username='aaquib')
    print(f'User: {user.username}, Email: {user.email}, Active: {user.is_active}')
    print(f'Password hash: {user.password}')

    # Try to authenticate
    auth_user = authenticate(username='aaquib', password='aaquib_1304')
    if auth_user:
        print('Authentication successful with aaquib_1304')
    else:
        print('Authentication failed with aaquib_1304')

    # Try with aaquib1304
    auth_user2 = authenticate(username='aaquib', password='aaquib1304')
    if auth_user2:
        print('Authentication successful with aaquib1304')
    else:
        print('Authentication failed with aaquib1304')

    # Try with email
    auth_user_email = authenticate(username='qureshiaaquib1304@gmail.com', password='aaquib_1304')
    if auth_user_email:
        print('Authentication with email successful')
    else:
        print('Authentication with email failed')

except User.DoesNotExist:
    print('User not found')
