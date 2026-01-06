from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Event
from .serializers import EventSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == 'admin':
                return Event.objects.all()
            elif user.role == 'organizer':
                return Event.objects.filter(organizer=user)
            else:  # student
                return Event.objects.filter(status='approved')
        else:
            # Anonymous users can only see approved events
            return Event.objects.filter(status='approved')

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if user.role == 'organizer' and instance.organizer != user:
            return Response({'error': 'You can only edit your own events'}, status=status.HTTP_403_FORBIDDEN)
        if user.role == 'organizer' and instance.status != 'pending':
            return Response({'error': 'You can only edit pending events'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if user.role == 'organizer' and instance.organizer != user:
            return Response({'error': 'You can only delete your own events'}, status=status.HTTP_403_FORBIDDEN)
        if user.role == 'organizer' and instance.status != 'pending':
            return Response({'error': 'You can only delete pending events'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):
        if request.user.role != 'admin':
            return Response({'error': 'Only admins can approve events'}, status=status.HTTP_403_FORBIDDEN)
        event = get_object_or_404(Event, pk=pk)
        event.status = 'approved'
        event.save()
        return Response({'message': 'Event approved'})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        if request.user.role != 'admin':
            return Response({'error': 'Only admins can reject events'}, status=status.HTTP_403_FORBIDDEN)
        event = get_object_or_404(Event, pk=pk)
        event.status = 'rejected'
        event.save()
        return Response({'message': 'Event rejected'})
