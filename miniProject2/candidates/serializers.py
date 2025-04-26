from rest_framework import serializers
from .models import Candidate
from users.serializers import UserProfileSerializer

class CandidateSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    skills = serializers.SerializerMethodField()

    class Meta:
        model = Candidate
        fields = ['id', 'user', 'skills', 'experience', 'education', 'resume', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_skills(self, obj):
        return [skill.strip() for skill in obj.skills.split(',') if skill.strip()] 