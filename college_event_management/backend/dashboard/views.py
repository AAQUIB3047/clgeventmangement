from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from events.models import Event
from registrations.models import Registration
from attendance.models import Attendance

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        total_events = Event.objects.count()
        total_registrations = Registration.objects.count()
        total_attendance = Attendance.objects.count()
        user_registrations = Registration.objects.filter(user=user).count()
        user_attendance = Attendance.objects.filter(registration__user=user).count()

        data = {
            'total_events': total_events,
            'total_registrations': total_registrations,
            'total_attendance': total_attendance,
            'user_registrations': user_registrations,
            'user_attendance': user_attendance,
        }
        return Response(data)
