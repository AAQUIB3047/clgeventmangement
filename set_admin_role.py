import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'college_event_management', 'backend'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from users.models import User

# Set role for user aaquib to admin
try:
    user = User.objects.get(username='aaquib')
    user.role = 'admin'
    user.save()
    print(f'User {user.username} set to role: {user.role}')
except User.DoesNotExist:
    print('User not found')
