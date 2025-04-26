from rest_framework import serializers
from .models import JobListing, JobCategory, JobApplication, JobCategoryMapping, JobMatch
from users.serializers import UserProfileSerializer

class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = '__all__'

class JobListingSerializer(serializers.ModelSerializer):
    categories = JobCategorySerializer(many=True, read_only=True)
    category_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    posted_by = UserProfileSerializer(read_only=True)

    class Meta:
        model = JobListing
        fields = '__all__'
        read_only_fields = ('posted_date', 'posted_by')

    def create(self, validated_data):
        category_ids = validated_data.pop('category_ids', [])
        job = JobListing.objects.create(**validated_data)
        for category_id in category_ids:
            JobCategoryMapping.objects.create(
                job=job,
                category_id=category_id
            )
        return job

    def validate_expiry_date(self, value):
        if value <= self.context['request'].user.date_joined:
            raise serializers.ValidationError("Expiry date must be in the future")
        return value

class JobApplicationSerializer(serializers.ModelSerializer):
    applicant = UserProfileSerializer(read_only=True)
    job = JobListingSerializer(read_only=True)
    
    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ('applied_date', 'applicant', 'match_score')
    
    def validate(self, data):
        if self.context['request'].user != data['resume'].user:
            raise serializers.ValidationError("You can only apply with your own resume")
        return data

class JobMatchSerializer(serializers.ModelSerializer):
    job = JobListingSerializer(read_only=True)
    
    class Meta:
        model = JobMatch
        fields = '__all__'
        read_only_fields = ('created_at',)

class JobApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ('job', 'resume', 'cover_letter')
    
    def validate(self, data):
        if self.context['request'].user != data['resume'].user:
            raise serializers.ValidationError("You can only apply with your own resume")
        return data 