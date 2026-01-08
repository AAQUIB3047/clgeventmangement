import os

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import GoogleAuthSerializer, UserSerializer

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', 'YOUR_GOOGLE_CLIENT_ID_HERE')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """
        Register a new student user.
        
        Expected payload:
        {
            "email": "student@example.com",
            "password": "securepassword123",
            "first_name": "John",
            "last_name": "Doe"
        }
        """
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            first_name = request.data.get('first_name', '')
            last_name = request.data.get('last_name', '')

            # Validation
            if not email or not password:
                return Response(
                    {"error": "Email and password are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if len(password) < 6:
                return Response(
                    {"error": "Password must be at least 6 characters long"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if user already exists
            if User.objects.filter(email=email).exists():
                return Response(
                    {"error": "Email already registered"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create new user
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role='student'
            )

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            user_data = UserSerializer(user).data

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': user_data,
                'message': 'Registration successful! You are now logged in.'
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": f"Registration failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """
        Login with email and password.
        
        Expected payload:
        {
            "email": "student@example.com",
            "password": "securepassword123"
        }
        """
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                return Response(
                    {"error": "Email and password are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get user
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {"error": "Invalid email or password"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Check password
            if not user.check_password(password):
                return Response(
                    {"error": "Invalid email or password"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user).data

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': user_data,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Login failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
                    # Token verification would be done here in production
                    # id_info = id_token.verify_oauth2_token(...)
                    pass
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
        
        # Get student information from Student model
        students = User.objects.filter(role='student').values(
            'id', 'email', 'first_name', 'last_name', 'branch', 'created_at'
        )
        return Response({
            'count': students.count(),
            'students': list(students)
        })
