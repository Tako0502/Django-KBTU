from rest_framework import serializers
from .models import Resume, ResumeAnalysis, ResumeFeedback, JobMatch
from users.serializers import UserProfileSerializer

class ResumeSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    analysis = serializers.SerializerMethodField()
    
    class Meta:
        model = Resume
        fields = '__all__'
        read_only_fields = ('status', 'analysis_result', 'score', 'upload_date', 'last_analyzed', 'ai_score', 'ai_feedback')
    
    def validate_file(self, value):
        if value.size > 10 * 1024 * 1024:  # 10MB limit
            raise serializers.ValidationError("File size should not exceed 10MB")
        return value

    def get_analysis(self, obj):
        analysis = ResumeAnalysis.objects.filter(resume=obj).first()
        if analysis:
            return {
                'analysis_date': analysis.analysis_date,
                'analysis_result': analysis.analysis_result,
                'score': analysis.score
            }
        return None

class ResumeAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeAnalysis
        fields = '__all__'
        read_only_fields = ('analysis_date',)

class ResumeFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeFeedback
        fields = '__all__'

class JobMatchSerializer(serializers.ModelSerializer):
    resume = ResumeSerializer(read_only=True)
    
    class Meta:
        model = JobMatch
        fields = '__all__'

class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ('title', 'file', 'is_public')
    
    def validate_file(self, value):
        if value.size > 10 * 1024 * 1024:  # 10MB limit
            raise serializers.ValidationError("File size should not exceed 10MB")
        return value

class ResumeAnalysisRequestSerializer(serializers.Serializer):
    resume_id = serializers.IntegerField()
    
    def validate_resume_id(self, value):
        try:
            Resume.objects.get(id=value)
        except Resume.DoesNotExist:
            raise serializers.ValidationError("Resume not found.")
        return value

class ResumeFeedbackRequestSerializer(serializers.Serializer):
    resume_id = serializers.IntegerField()
    
    def validate_resume_id(self, value):
        try:
            Resume.objects.get(id=value)
        except Resume.DoesNotExist:
            raise serializers.ValidationError("Resume not found.")
        return value

class JobMatchRequestSerializer(serializers.Serializer):
    resume_id = serializers.IntegerField()
    job_id = serializers.IntegerField()
    
    def validate(self, data):
        try:
            Resume.objects.get(id=data['resume_id'])
        except Resume.DoesNotExist:
            raise serializers.ValidationError({"resume_id": "Resume not found."})
        
        try:
            from jobs.models import Job
            Job.objects.get(id=data['job_id'])
        except Job.DoesNotExist:
            raise serializers.ValidationError({"job_id": "Job not found."})
        
        return data

class ResumeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ('title', 'is_public', 'skills')
    
    def validate_skills(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Skills must be a list")
        return value 