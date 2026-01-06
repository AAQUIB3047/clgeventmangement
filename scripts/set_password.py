import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'college_event_management', 'backend'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from users.models import User

try:
    u = User.objects.get(username='admin')
    u.set_password('admin123')
    u.save()
    print('Password set for admin to admin123')
except User.DoesNotExist:
    print('Admin user not found')
