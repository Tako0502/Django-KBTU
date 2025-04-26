from django.db import models
from users.models import User

class ResumeAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resume_analyses')
    resume_file = models.FileField(upload_to='resumes/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Extracted Information
    skills = models.JSONField(default=list)
    experience = models.JSONField(default=list)
    education = models.JSONField(default=list)
    
    # Analysis Results
    overall_score = models.FloatField(default=0.0)
    ats_compatibility = models.FloatField(default=0.0)
    formatting_score = models.FloatField(default=0.0)
    
    # Feedback and Recommendations
    skill_gaps = models.JSONField(default=list)
    formatting_suggestions = models.JSONField(default=list)
    keyword_suggestions = models.JSONField(default=list)
    
    class Meta:
        db_table = 'resume_analysis'
        ordering = ['-created_at']

class JobMatch(models.Model):
    resume_analysis = models.ForeignKey(ResumeAnalysis, on_delete=models.CASCADE, related_name='job_matches')
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    match_score = models.FloatField(default=0.0)
    matched_skills = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ai_processing_job_matches'
        ordering = ['-match_score'] 