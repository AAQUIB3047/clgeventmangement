import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'college_event_management', 'backend'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from users.models import User

# Check if user already exists
if User.objects.filter(email='qureshiaaquib1304@gmail.com').exists():
    print('User with this email already exists.')
else:
    # Create new user
    user = User.objects.create_user(
        username='aaquib',  # Using 'aaquib' as username
        email='qureshiaaquib1304@gmail.com',
        password='aaquib_1304'
    )
    print(f'User created: Username: {user.username}, Email: {user.email}')
