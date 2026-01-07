import os
from datetime import datetime, timedelta

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from django.contrib.auth.models import User
from events.models import Event

# Create admin user if not exists
admin, created = User.objects.get_or_create(username='admin')
if created:
    admin.set_password('admin123')
    admin.email = 'admin@example.com'
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()
    print("✅ Admin user created")
else:
    print("ℹ️  Admin user already exists")

# Create test user
student, created = User.objects.get_or_create(username='student1')
if created:
    student.set_password('student123')
    student.email = 'student@example.com'
    student.save()
    print("✅ Student user created")
else:
    print("ℹ️  Student user already exists")

# Create sample events
events_data = [
    {
        'title': 'Tech Conference 2026',
        'description': 'A comprehensive tech conference covering latest trends in web development, AI, and cloud computing.',
        'date': datetime.now() + timedelta(days=30),
        'location': 'Conference Hall A',
        'capacity': 100,
        'status': 'approved'
    },
    {
        'title': 'Django Workshop',
        'description': 'Learn Django framework from basics to advanced concepts. Perfect for beginners and intermediate developers.',
        'date': datetime.now() + timedelta(days=15),
        'location': 'Computer Lab B',
        'capacity': 50,
        'status': 'approved'
    },
    {
        'title': 'React Bootcamp',
        'description': 'Intensive 2-week bootcamp on React.js, covering components, hooks, and state management.',
        'date': datetime.now() + timedelta(days=45),
        'location': 'Room 301',
        'capacity': 30,
        'status': 'approved'
    },
    {
        'title': 'Career Fair',
        'description': 'Meet with top companies and discuss internship and job opportunities.',
        'date': datetime.now() + timedelta(days=60),
        'location': 'Main Auditorium',
        'capacity': 500,
        'status': 'approved'
    },
]

created_count = 0
for event_data in events_data:
    event, created = Event.objects.get_or_create(
        title=event_data['title'],
        defaults={
            'description': event_data['description'],
            'date': event_data['date'],
            'location': event_data['location'],
            'capacity': event_data['capacity'],
            'organizer': admin,
            'status': event_data['status']
        }
    )
    if created:
        created_count += 1
        print(f"✅ Event created: {event.title}")
    else:
        print(f"ℹ️  Event already exists: {event.title}")

if created_count > 0:
    print(f"\n✨ {created_count} new events created!")
else:
    print("\n✨ Sample data already in database")

print("\n📊 Database Summary:")
print(f"- Total Users: {User.objects.count()}")
print(f"- Total Events: {Event.objects.count()}")
