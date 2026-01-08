from attendance.models import Attendance
from django.core.mail import send_mail
from django.db.models import Count
from django.utils import timezone
from events.models import Event
from events.serializers import EventSerializer
from registrations.models import Registration
from registrations.serializers import RegistrationSerializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from users.models import AuditLog, Department, User


class IsAdmin(IsAuthenticated):
    """Custom permission to check if user is admin"""
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'admin'


class AdminDashboardView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        """Get comprehensive admin dashboard data"""
        now = timezone.now()
        
        # Statistics
        total_events = Event.objects.count()
        active_events = Event.objects.filter(status__in=['published', 'ongoing']).count()
        total_registrations = Registration.objects.count()
        pending_approvals = Registration.objects.filter(status='pending').count()
        total_students = User.objects.filter(role='student').count()
        total_faculty = User.objects.filter(role='faculty').count()
        total_departments = Department.objects.count()
        
        # Revenue (paid events)
        paid_registrations = Registration.objects.filter(payment_status='completed')
        total_revenue = sum(
            event.registration_fee * paid_registrations.filter(event=event).count()
            for event in Event.objects.filter(registration_fee__gt=0)
        )
        
        # Upcoming events
        upcoming_events = Event.objects.filter(
            event_date__gte=now.date()
        ).order_by('event_date')[:5]
        
        # Events happening today
        today_events = Event.objects.filter(event_date=now.date())
        
        # Recent registrations
        recent_registrations = Registration.objects.select_related(
            'student', 'event'
        ).order_by('-registration_time')[:10]
        
        # Registrations by status
        registration_stats = Registration.objects.values('status').annotate(count=Count('id'))
        
        # Top events by registration count
        top_events = Event.objects.annotate(
            registration_count=Count('registrations')
        ).order_by('-registration_count')[:5]

        dashboard_data = {
            'statistics': {
                'total_events': total_events,
                'active_events': active_events,
                'total_registrations': total_registrations,
                'pending_approvals': pending_approvals,
                'total_students': total_students,
                'total_faculty': total_faculty,
                'total_departments': total_departments,
                'total_revenue': float(total_revenue),
            },
            'upcoming_events': EventSerializer(upcoming_events, many=True).data,
            'today_events': EventSerializer(today_events, many=True).data,
            'recent_registrations': RegistrationSerializer(recent_registrations, many=True).data,
            'registration_stats': list(registration_stats),
            'top_events': EventSerializer(top_events, many=True).data,
        }
        
        # Log dashboard access
        AuditLog.objects.create(
            admin=request.user,
            action_type='view',
            entity_type='Dashboard',
            entity_id=0,
            description='Accessed admin dashboard',
            ip_address=self.get_client_ip(request)
        )
        
        return Response(dashboard_data)
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class EventManagementViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdmin]

    def create(self, request, *args, **kwargs):
        """Create a new event with full details"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Set created_by to current admin
        event = serializer.save(created_by=request.user, department=request.user.department or Department.objects.first())
        
        # Log action
        AuditLog.objects.create(
            admin=request.user,
            action_type='create',
            entity_type='Event',
            entity_id=event.id,
            description=f'Created event: {event.title}',
            ip_address=self.get_client_ip(request)
        )
        
        return Response(EventSerializer(event).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Update event details"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        
        # Log action
        AuditLog.objects.create(
            admin=request.user,
            action_type='update',
            entity_type='Event',
            entity_id=event.id,
            description=f'Updated event: {event.title}',
            ip_address=self.get_client_ip(request)
        )
        
        return Response(EventSerializer(event).data)

    def destroy(self, request, *args, **kwargs):
        """Delete an event"""
        instance = self.get_object()
        event_name = instance.title
        
        # Check registrations
        registration_count = instance.registrations.count()
        
        # Log action before deletion
        AuditLog.objects.create(
            admin=request.user,
            action_type='delete',
            entity_type='Event',
            entity_id=instance.id,
            description=f'Deleted event: {event_name} (had {registration_count} registrations)',
            ip_address=self.get_client_ip(request)
        )
        
        instance.delete()
        return Response(
            {'message': 'Event deleted successfully', 'registrations_affected': registration_count},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publish an event"""
        event = self.get_object()
        event.status = 'published'
        event.save()
        
        AuditLog.objects.create(
            admin=request.user,
            action_type='approve',
            entity_type='Event',
            entity_id=event.id,
            description=f'Published event: {event.title}',
            ip_address=self.get_client_ip(request)
        )
        
        return Response({'message': 'Event published', 'event': EventSerializer(event).data})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an event instead of deleting"""
        event = self.get_object()
        event.status = 'cancelled'
        event.save()
        
        # Send cancellation emails to all registered students
        registrations = event.registrations.filter(status='confirmed')
        for reg in registrations:
            self.send_cancellation_email(event, reg.student)
        
        AuditLog.objects.create(
            admin=request.user,
            action_type='reject',
            entity_type='Event',
            entity_id=event.id,
            description=f'Cancelled event: {event.title}',
            ip_address=self.get_client_ip(request)
        )
        
        return Response({
            'message': 'Event cancelled',
            'notifications_sent': registrations.count(),
            'event': EventSerializer(event).data
        })

    @action(detail=True, methods=['get'])
    def registrations(self, request, pk=None):
        """Get all registrations for an event"""
        event = self.get_object()
        registrations = event.registrations.all()
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def approve_registrations(self, request, pk=None):
        """Approve selected registrations"""
        event = self.get_object()
        registration_ids = request.data.get('registration_ids', [])
        
        registrations = event.registrations.filter(id__in=registration_ids, status='pending')
        count = registrations.update(status='confirmed')
        
        AuditLog.objects.create(
            admin=request.user,
            action_type='approve',
            entity_type='Registration',
            entity_id=event.id,
            description=f'Approved {count} registrations for event: {event.title}',
            ip_address=self.get_client_ip(request)
        )
        
        return Response({'message': f'Approved {count} registrations'})

    @action(detail=True, methods=['post'])
    def reject_registrations(self, request, pk=None):
        """Reject selected registrations"""
        event = self.get_object()
        registration_ids = request.data.get('registration_ids', [])
        reason = request.data.get('reason', 'Does not meet criteria')
        
        registrations = event.registrations.filter(id__in=registration_ids)
        for reg in registrations:
            if reg.status == 'pending':
                reg.status = 'cancelled'
                reg.save()
                # Send rejection email
                self.send_rejection_email(event, reg.student, reason)
        
        AuditLog.objects.create(
            admin=request.user,
            action_type='reject',
            entity_type='Registration',
            entity_id=event.id,
            description=f'Rejected registrations for event: {event.title}. Reason: {reason}',
            ip_address=self.get_client_ip(request)
        )
        
        return Response({'message': f'Rejected {len(registration_ids)} registrations'})

    @action(detail=True, methods=['post'])
    def add_manual_registration(self, request, pk=None):
        """Manually register a student for an event"""
        event = self.get_object()
        student_id = request.data.get('student_id')
        
        try:
            student = User.objects.get(id=student_id, role='student')
        except User.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        
        registration, created = Registration.objects.get_or_create(
            event=event,
            student=student,
            defaults={'status': 'confirmed'}
        )
        
        if not created:
            return Response(
                {'error': 'Student is already registered'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        AuditLog.objects.create(
            admin=request.user,
            action_type='create',
            entity_type='Registration',
            entity_id=registration.id,
            description=f'Manually registered {student.get_full_name()} for {event.title}',
            ip_address=self.get_client_ip(request)
        )
        
        return Response(RegistrationSerializer(registration).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def mark_attendance(self, request, pk=None):
        """Mark student attendance for event"""
        event = self.get_object()
        student_id = request.data.get('student_id')
        verification_method = request.data.get('verification_method', 'manual')
        
        try:
            student = User.objects.get(id=student_id, role='student')
        except User.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        
        attendance, created = Attendance.objects.get_or_create(
            event=event,
            student=student,
            defaults={
                'check_in_time': timezone.now(),
                'verification_method': verification_method
            }
        )
        
        if not created:
            attendance.check_in_time = timezone.now()
            attendance.save()
        
        AuditLog.objects.create(
            admin=request.user,
            action_type='update',
            entity_type='Attendance',
            entity_id=attendance.id,
            description=f'Marked attendance for {student.get_full_name()} at {event.title}',
            ip_address=self.get_client_ip(request)
        )
        
        return Response({'message': 'Attendance marked', 'attendance_id': attendance.id})

    @action(detail=True, methods=['get'])
    def export_registrations(self, request, pk=None):
        """Export registrations as CSV"""
        import csv

        from django.http import HttpResponse
        
        event = self.get_object()
        registrations = event.registrations.all()
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{event.title}_registrations.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Roll Number', 'Name', 'Email', 'Department', 'Status', 'Registration Date'])
        
        for reg in registrations:
            student = reg.student
            writer.writerow([
                student.username,
                student.get_full_name(),
                student.email,
                student.department or '',
                reg.status,
                reg.registration_time.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        AuditLog.objects.create(
            admin=request.user,
            action_type='view',
            entity_type='Registration',
            entity_id=event.id,
            description=f'Exported registrations for {event.title}',
            ip_address=self.get_client_ip(request)
        )
        
        return response

    def send_cancellation_email(self, event, student):
        """Send event cancellation email to student"""
        subject = f"Event Cancelled: {event.title}"
        message = f"""
        Dear {student.get_full_name()},
        
        The following event has been cancelled:
        Event: {event.title}
        Originally Scheduled: {event.event_date} from {event.start_time} to {event.end_time}
        
        We apologize for any inconvenience caused.
        
        Best regards,
        Event Management Team
        """
        send_mail(subject, message, 'admin@eventmanagement.com', [student.email], fail_silently=True)

    def send_rejection_email(self, event, student, reason):
        """Send registration rejection email to student"""
        subject = f"Registration Update: {event.title}"
        message = f"""
        Dear {student.get_full_name()},
        
        Your registration for the following event could not be approved:
        Event: {event.title}
        Reason: {reason}
        
        Please contact the organizers if you have any questions.
        
        Best regards,
        Event Management Team
        """
        send_mail(subject, message, 'admin@eventmanagement.com', [student.email], fail_silently=True)

    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
