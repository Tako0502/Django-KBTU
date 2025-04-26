from rest_framework import serializers
from resumes.models import Resume, ResumeAnalysis, ResumeFeedback, JobMatch
from jobs.models import JobListing

class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ('file', 'title', 'is_public')
    
    def validate_file(self, value):
        if value.size > 10 * 1024 * 1024:  # 10MB limit
            raise serializers.ValidationError("File size should not exceed 10MB")
        return value

class ResumeAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeAnalysis
        fields = '__all__'
        read_only_fields = ('analysis_date',)

class ResumeFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeFeedback
        fields = '__all__'
        read_only_fields = ('created_at',)

class JobMatchSerializer(serializers.ModelSerializer):
    job = serializers.SerializerMethodField()
    
    class Meta:
        model = JobMatch
        fields = '__all__'
        read_only_fields = ('created_at',)
    
    def get_job(self, obj):
        from jobs.serializers import JobListingSerializer
        return JobListingSerializer(obj.job).data

class ResumeAnalysisRequestSerializer(serializers.Serializer):
    resume = serializers.PrimaryKeyRelatedField(queryset=Resume.objects.all())

class AnalysisRequestSerializer(serializers.Serializer):
    resume_id = serializers.IntegerField()
    
    def validate_resume_id(self, value):
        try:
            Resume.objects.get(id=value)
        except Resume.DoesNotExist:
            raise serializers.ValidationError("Resume not found.")
        return value

class FeedbackRequestSerializer(serializers.Serializer):
    resume_id = serializers.IntegerField()
    
    def validate_resume_id(self, value):
        try:
            Resume.objects.get(id=value)
        except Resume.DoesNotExist:
            raise serializers.ValidationError("Resume not found.")
        return value

class MatchRequestSerializer(serializers.Serializer):
    resume_id = serializers.IntegerField()
    
    def validate_resume_id(self, value):
        try:
            Resume.objects.get(id=value)
        except Resume.DoesNotExist:
            raise serializers.ValidationError("Resume not found.")
        return value 