import os
import sys
import django
from datetime import date, time

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'college_event_management', 'backend'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from events.models import Event
from users.models import User

def create_test_events():
    # Get the admin user
    try:
        admin_user = User.objects.get(username='aaquib')
    except User.DoesNotExist:
        print('Admin user not found')
        return

    # Create test events
    events_data = [
        {
            'title': 'Tech Conference 2025',
            'description': 'Annual technology conference featuring latest innovations',
            'date': date(2025, 12, 25),
            'start_time': time(9, 0),
            'end_time': time(17, 0),
            'location': 'Main Auditorium',
            'capacity': 200,
            'status': 'approved'
        },
        {
            'title': 'Cultural Fest',
            'description': 'College cultural festival with music, dance and drama',
            'date': date(2025, 12, 26),
            'start_time': time(10, 0),
            'end_time': time(20, 0),
            'location': 'College Ground',
            'capacity': 500,
            'status': 'approved'
        },
        {
            'title': 'Workshop on AI',
            'description': 'Hands-on workshop on Artificial Intelligence fundamentals',
            'date': date(2025, 12, 27),
            'start_time': time(14, 0),
            'end_time': time(18, 0),
            'location': 'Computer Lab',
            'capacity': 50,
            'status': 'pending'
        }
    ]

    for event_data in events_data:
        event, created = Event.objects.get_or_create(
            title=event_data['title'],
            defaults={
                **event_data,
                'organizer': admin_user
            }
        )
        if created:
            print(f'Created event: {event.title}')
        else:
            print(f'Event already exists: {event.title}')

if __name__ == '__main__':
    create_test_events()
