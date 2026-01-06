import json
import os

from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import StudentEnrollment, User
from .serializers import GoogleAuthSerializer, UserSerializer

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', 'YOUR_GOOGLE_CLIENT_ID_HERE')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def google_login(self, request):
        """
        Handle Google OAuth login.
        
        Expected payload:
        {
            "token": "google_id_token",
            "name": "User Full Name",
            "email": "user@example.com",
            "picture": "https://...",
            "branch": "cse"  // optional
        }
        """
        serializer = GoogleAuthSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # For development: skip token verification if GOOGLE_CLIENT_ID not set
            # In production, verify the token with Google
            if GOOGLE_CLIENT_ID != 'YOUR_GOOGLE_CLIENT_ID_HERE':
                try:
                    id_info = id_token.verify_oauth2_token(
                        serializer.validated_data['token'],
                        requests.Request(),
                        GOOGLE_CLIENT_ID
                    )
                except Exception as e:
                    return Response(
                        {"error": f"Token verification failed: {str(e)}"},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            
            # Create or update user
            user, created = serializer.create_or_update_user()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            user_data = UserSerializer(user).data
            
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': user_data,
                'message': 'Google login successful'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": f"Google login failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def enrollments(self, request):
        """Get all student enrollments (for admin)"""
        if request.user.role != 'admin':
            return Response(
                {"error": "Only admins can access this endpoint"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        enrollments = StudentEnrollment.objects.all().values(
            'id', 'email', 'full_name', 'branch', 'roll_number', 'created_at'
        )
        return Response({
            'count': enrollments.count(),
            'enrollments': list(enrollments)
        })
