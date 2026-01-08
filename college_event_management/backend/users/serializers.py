from rest_framework import serializers

from .models import Department, Faculty, Student, User


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name', 'department_code', 'head_of_department']
        read_only_fields = ['id']


class StudentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = ['id', 'user', 'roll_number', 'year', 'department', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_user(self, obj):
        return UserSerializer(obj.user).data


class FacultySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = Faculty
        fields = ['id', 'user', 'employee_id', 'designation', 'department', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_user(self, obj):
        return UserSerializer(obj.user).data


class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'role', 
                  'phone_number', 'branch', 'department', 'department_id', 'is_google_user', 
                  'profile_picture', 'is_active', 'created_at']
        read_only_fields = ['id', 'is_google_user', 'profile_picture', 'created_at']


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
        
        return user, created
