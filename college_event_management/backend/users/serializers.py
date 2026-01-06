from rest_framework import serializers

from .models import StudentEnrollment, User


class StudentEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEnrollment
        fields = ['id', 'email', 'full_name', 'branch', 'roll_number', 'created_at']
        read_only_fields = ['created_at']


class UserSerializer(serializers.ModelSerializer):
    enrollment = StudentEnrollmentSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'role', 
                  'phone_number', 'branch', 'department', 'is_google_user', 
                  'profile_picture', 'enrollment']
        read_only_fields = ['id', 'is_google_user', 'profile_picture']


class GoogleAuthSerializer(serializers.Serializer):
    """Serializer for Google OAuth token verification"""
    token = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    picture = serializers.CharField(required=False, allow_blank=True)
    branch = serializers.ChoiceField(choices=User.BRANCH_CHOICES, required=False, allow_blank=True)

    def validate_token(self, value):
        if not value:
            raise serializers.ValidationError("Token is required")
        return value

    def create_or_update_user(self):
        """Create or update user from Google auth data"""
        data = self.validated_data
        email = data['email']
        name_parts = data['name'].split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        user, created = User.objects.update_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'username': email.split('@')[0],
                'is_google_user': True,
                'profile_picture': data.get('picture', ''),
                'branch': data.get('branch', 'other'),
            }
        )
        
        # Create or update StudentEnrollment
        StudentEnrollment.objects.update_or_create(
            user=user,
            defaults={
                'email': email,
                'full_name': data['name'],
                'branch': data.get('branch', 'other'),
            }
        )
        
        return user, created
