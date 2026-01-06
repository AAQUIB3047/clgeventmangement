import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from users.models import User

user = User.objects.filter(email='qureshiaaquib1304@gmail.com').first()
if user:
    print(f"✓ User found: {user.username}")
    print(f"  Email: {user.email}")
    print(f"  Is Staff: {user.is_staff}")
    print(f"  Is Superuser: {user.is_superuser}")
    print(f"  Role: {user.role}")
    print(f"  Password check: {user.check_password('aaquib1304')}")
else:
    print("✗ User not found")
    print(f"Available users: {list(User.objects.all().values('username', 'email'))}")
