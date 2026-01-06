from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Registration
from .serializers import RegistrationSerializer

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]
