from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'code', 
                  'host', 'guest_can_pause', 'votes_to_skip', 'created_at')
    
class CreateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields= ('guest_can_pause', 'votes_to_skip')