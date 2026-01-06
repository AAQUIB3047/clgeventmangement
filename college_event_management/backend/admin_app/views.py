from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from events.models import Event
from registrations.models import Registration
from attendance.models import Attendance
from django.utils import timezone
from datetime import timedelta
from users.serializers import UserSerializer
from events.serializers import EventSerializer

class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'admin':
            return Response({'error': 'Access denied'}, status=403)

        # Get dashboard statistics directly from Django models
        total_users = User.objects.count()
        total_events = Event.objects.count()
        total_registrations = Registration.objects.count()
        total_attendance = Attendance.objects.count()

        # Get recent events
        recent_events = Event.objects.order_by('-date')[:5].values('id', 'title', 'date', 'status')

        # Get upcoming events
        upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:5]

        dashboard_data = {
            'total_users': total_users,
            'total_events': total_events,
            'total_registrations': total_registrations,
            'total_attendance': total_attendance,
            'recent_events': list(recent_events),
            'upcoming_events': list(upcoming_events.values('id', 'title', 'date', 'status'))
        }

        return Response(dashboard_data)

class ManageUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'admin':
            return Response({'error': 'Access denied'}, status=403)
        users = User.objects.all().values('id', 'username', 'email', 'role', 'department', 'date_joined')
        return Response(list(users))

    def post(self, request):
        if request.user.role != 'admin':
            return Response({'error': 'Access denied'}, status=403)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        if request.user.role != 'admin':
            return Response({'error': 'Access denied'}, status=403)
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({'message': 'User deleted'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

class ManageEventsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'admin':
            return Response({'error': 'Access denied'}, status=403)
        events = Event.objects.all().values('id', 'title', 'description', 'date', 'status', 'organizer__username')
        return Response(list(events))

    def post(self, request):
        if request.user.role != 'admin':
            return Response({'error': 'Access denied'}, status=403)
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk):
        if request.user.role != 'admin':
            return Response({'error': 'Access denied'}, status=403)
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=404)

    def delete(self, request, pk):
        if request.user.role != 'admin':
            return Response({'error': 'Access denied'}, status=403)
        try:
            event = Event.objects.get(pk=pk)
            event.delete()
            return Response({'message': 'Event deleted'})
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=404)
