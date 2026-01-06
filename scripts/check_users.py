import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'college_event_management', 'backend'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from users.models import User

users = User.objects.all()
print('Users:')
for u in users:
    print(f'ID: {u.id}, Username: {u.username}, Email: {u.email}')
