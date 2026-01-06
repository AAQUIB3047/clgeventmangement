import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'college_event_management', 'backend'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from users.models import User

# Set password for user aaquib
try:
    user = User.objects.get(username='aaquib')
    user.set_password('aaquib_1304')
    user.save()
    print(f'Password set for user {user.username} to aaquib_1304')
except User.DoesNotExist:
    print('User not found')
