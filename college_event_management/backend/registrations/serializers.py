from rest_framework import serializers

from .models import Registration


class RegistrationSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    student_email = serializers.CharField(source='student.email', read_only=True)
    student_roll = serializers.CharField(source='student.username', read_only=True)
    
    class Meta:
        model = Registration
        fields = [
            'id', 'event', 'event_title', 'student', 'student_name', 'student_email',
            'student_roll', 'registration_time', 'status', 'payment_status', 
            'transaction_id', 'attended', 'updated_at'
        ]
        read_only_fields = ['id', 'registration_time', 'updated_at']
