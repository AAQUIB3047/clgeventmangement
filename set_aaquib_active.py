import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'college_event_management', 'backend'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from users.models import User

# Set user aaquib to active
try:
    user = User.objects.get(username='aaquib')
    user.is_active = True
    user.save()
    print(f'User {user.username} set to active: {user.is_active}')
except User.DoesNotExist:
    print('User not found')
