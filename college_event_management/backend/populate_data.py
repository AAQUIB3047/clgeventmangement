#!/usr/bin/env python
"""
Script to populate sample data for College Event Management System
Run with: python manage.py shell < populate_data.py
"""

import os
from datetime import timedelta

import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from events.models import Category, Event, Venue
from users.models import Department, Faculty, Student, User

print("=" * 60)
print("SETTING UP SAMPLE DATA FOR COLLEGE EVENT MANAGEMENT")
print("=" * 60)

# Create Departments
print("\n1. Creating Departments...")
departments_data = [
    {'name': 'Computer Science & Engineering', 'code': 'CSE'},
    {'name': 'Electronics & Communication', 'code': 'ECE'},
    {'name': 'Mechanical Engineering', 'code': 'ME'},
    {'name': 'Civil Engineering', 'code': 'CE'},
    {'name': 'Information Technology', 'code': 'IT'},
]

departments = {}
for dept_data in departments_data:
    dept, created = Department.objects.get_or_create(
        department_code=dept_data['code'],
        defaults={
            'department_name': dept_data['name'],
            'head_of_department': f"Dr. {dept_data['code']} Head"
        }
    )
    departments[dept_data['code']] = dept
    status = "✓ Created" if created else "✓ Exists"
    print(f"  {status}: {dept.department_name}")

# Create Faculty Users
print("\n2. Creating Faculty Users...")
faculty_data = [
    {'name': 'Dr. John Smith', 'email': 'john.smith@college.edu', 'dept': 'CSE', 'emp_id': 'F001'},
    {'name': 'Dr. Sarah Johnson', 'email': 'sarah.johnson@college.edu', 'dept': 'ECE', 'emp_id': 'F002'},
    {'name': 'Dr. Mike Wilson', 'email': 'mike.wilson@college.edu', 'dept': 'ME', 'emp_id': 'F003'},
]

for faculty_info in faculty_data:
    user, created = User.objects.get_or_create(
        email=faculty_info['email'],
        defaults={
            'username': faculty_info['email'].split('@')[0],
            'first_name': faculty_info['name'].split()[1],
            'last_name': faculty_info['name'].split()[2] if len(faculty_info['name'].split()) > 2 else '',
            'role': 'faculty',
            'department': departments[faculty_info['dept']],
            'is_active': True
        }
    )
    if created:
        user.set_password('faculty123')
        user.save()
        Faculty.objects.create(
            user=user,
            employee_id=faculty_info['emp_id'],
            designation='Assistant Professor',
            department=departments[faculty_info['dept']]
        )
    print(f"  ✓ {faculty_info['name']} ({faculty_info['email']})")

# Create Student Users
print("\n3. Creating Student Users...")
student_data = [
    {'name': 'Aaquib Qureshi', 'email': 'aaquib@college.edu', 'roll': 'CSE001', 'dept': 'CSE', 'year': 3},
    {'name': 'Raj Kumar', 'email': 'raj@college.edu', 'roll': 'CSE002', 'dept': 'CSE', 'year': 2},
    {'name': 'Priya Sharma', 'email': 'priya@college.edu', 'roll': 'ECE001', 'dept': 'ECE', 'year': 3},
    {'name': 'Vikram Singh', 'email': 'vikram@college.edu', 'roll': 'ME001', 'dept': 'ME', 'year': 1},
]

for student_info in student_data:
    user, created = User.objects.get_or_create(
        email=student_info['email'],
        defaults={
            'username': student_info['email'].split('@')[0],
            'first_name': student_info['name'].split()[0],
            'last_name': student_info['name'].split()[1] if len(student_info['name'].split()) > 1 else '',
            'role': 'student',
            'department': departments[student_info['dept']],
            'branch': 'cse' if student_info['dept'] == 'CSE' else 'other',
            'is_active': True
        }
    )
    if created:
        user.set_password('student123')
        user.save()
        Student.objects.create(
            user=user,
            roll_number=student_info['roll'],
            year=student_info['year'],
            department=departments[student_info['dept']]
        )
    print(f"  ✓ {student_info['name']} ({student_info['roll']})")

# Create Organizer Users
print("\n4. Creating Event Organizer Users...")
organizer_data = [
    {'name': 'Event Manager', 'email': 'organizer@college.edu'},
]

for org_info in organizer_data:
    user, created = User.objects.get_or_create(
        email=org_info['email'],
        defaults={
            'username': org_info['email'].split('@')[0],
            'first_name': org_info['name'].split()[0],
            'last_name': org_info['name'].split()[1] if len(org_info['name'].split()) > 1 else '',
            'role': 'organizer',
            'is_active': True
        }
    )
    if created:
        user.set_password('organizer123')
        user.save()
    print(f"  ✓ {org_info['name']} ({org_info['email']})")

# Create Venues
print("\n5. Creating Venues...")
venue_data = [
    {'name': 'Main Auditorium', 'capacity': 500},
    {'name': 'Seminar Hall A', 'capacity': 100},
    {'name': 'Seminar Hall B', 'capacity': 100},
    {'name': 'Outdoor Grounds', 'capacity': 1000},
]

venues = {}
for venue_info in venue_data:
    venue, created = Venue.objects.get_or_create(
        venue_name=venue_info['name'],
        defaults={'capacity': venue_info['capacity']}
    )
    venues[venue_info['name']] = venue
    status = "✓ Created" if created else "✓ Exists"
    print(f"  {status}: {venue.venue_name} (Capacity: {venue.capacity})")

# Create Categories
print("\n6. Creating Event Categories...")
category_data = ['Technical', 'Cultural', 'Sports', 'Workshop', 'Seminar']

categories = {}
for cat_name in category_data:
    cat, created = Category.objects.get_or_create(
        category_name=cat_name
    )
    categories[cat_name] = cat
    status = "✓ Created" if created else "✓ Exists"
    print(f"  {status}: {cat.category_name}")

# Create Sample Events
print("\n7. Creating Sample Events...")
try:
    admin_user = User.objects.get(email='admin@example.com')
    admin_dept = departments['CSE']
except User.DoesNotExist:
    print("  ⚠ Admin user not found!")
    admin_user = None

if admin_user:
    event_data = [
        {
            'title': 'Annual Tech Summit 2026',
            'description': 'Join us for the biggest tech conference of the year with industry leaders discussing AI, Cloud Computing, and Web Development.',
            'date_offset': 7,
            'start_hour': 9,
            'duration_hours': 8,
            'venue': 'Main Auditorium',
            'category': 'Technical',
            'type': 'conference',
            'capacity': 500
        },
        {
            'title': 'Web Development Workshop',
            'description': 'Learn modern web development with React and Django. Hands-on coding session for beginners to intermediate level developers.',
            'date_offset': 14,
            'start_hour': 10,
            'duration_hours': 4,
            'venue': 'Seminar Hall A',
            'category': 'Workshop',
            'type': 'workshop',
            'capacity': 100
        },
        {
            'title': 'Cultural Fest 2026',
            'description': 'Celebrate our diverse culture with music, dance, drama, and performances from around the world.',
            'date_offset': 21,
            'start_hour': 18,
            'duration_hours': 4,
            'venue': 'Outdoor Grounds',
            'category': 'Cultural',
            'type': 'cultural',
            'capacity': 1000
        },
        {
            'title': 'AI & Machine Learning Seminar',
            'description': 'Explore the latest trends in AI and ML with expert speakers from leading tech companies.',
            'date_offset': 10,
            'start_hour': 14,
            'duration_hours': 3,
            'venue': 'Seminar Hall B',
            'category': 'Seminar',
            'type': 'seminar',
            'capacity': 100
        },
    ]

    from datetime import datetime, time
    for event_info in event_data:
        event_date = timezone.now().date() + timedelta(days=event_info['date_offset'])
        start_time = time(event_info['start_hour'], 0)
        end_time = time((event_info['start_hour'] + event_info['duration_hours']) % 24, 0)
        
        event, created = Event.objects.get_or_create(
            title=event_info['title'],
            event_date=event_date,
            defaults={
                'description': event_info['description'],
                'start_time': start_time,
                'end_time': end_time,
                'venue': venues[event_info['venue']],
                'category': categories[event_info['category']],
                'department': admin_dept,
                'event_type': event_info['type'],
                'max_capacity': event_info['capacity'],
                'created_by': admin_user,
                'status': 'published'
            }
        )
        status = "✓ Created" if created else "✓ Exists"
        print(f"  {status}: {event.title}")

print("\n" + "=" * 60)
print("SETUP COMPLETE!")
print("=" * 60)
print("\n📋 SAMPLE ACCOUNTS CREATED:\n")
print("ADMIN:")
print("  Email: admin@example.com | Password: admin123\n")
print("FACULTY:")
for faculty_info in faculty_data:
    print(f"  Email: {faculty_info['email']} | Password: faculty123")
print()
print("STUDENTS:")
for student_info in student_data:
    print(f"  Email: {student_info['email']} | Password: student123")
print()
print("ORGANIZER:")
for org_info in organizer_data:
    print(f"  Email: {org_info['email']} | Password: organizer123")
print("\n" + "=" * 60)
print("🚀 APPLICATION READY!")
print("=" * 60)
print("\n✅ Backend: http://localhost:8000")
print("✅ Frontend: http://localhost:3000")
print("✅ Admin Panel: http://localhost:8000/admin")
print("\n" + "=" * 60)
