from django.db import models
from django.conf import settings
from django.utils import timezone
from .validators import validate_file_extension

class Resume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='resumes/', validators=[validate_file_extension])
    upload_date = models.DateTimeField(default=timezone.now)
    is_public = models.BooleanField(default=True)
    last_analyzed = models.DateTimeField(null=True, blank=True)
    
    # Basic information extracted from resume
    full_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=255, blank=True)
    
    # Education and Experience (stored as JSON in MongoDB)
    education = models.JSONField(default=dict, blank=True)
    experience = models.JSONField(default=dict, blank=True)
    skills = models.JSONField(default=list, blank=True)
    
    # AI Analysis Results
    ai_score = models.FloatField(null=True, blank=True)
    ai_feedback = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-upload_date']
        db_table = 'resumes'
    
    def __str__(self):
        return f"{self.title} - {self.user.email}"
    
    def get_skills_list(self):
        return self.skills if isinstance(self.skills, list) else []
    
    def update_analysis(self, score, feedback):
        self.ai_score = score
        self.ai_feedback = feedback
        self.last_analyzed = timezone.now()
        self.save()

class ResumeAnalysis(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='analysis')
    analysis_date = models.DateTimeField(default=timezone.now)
    skill_gaps = models.JSONField(default=list)
    formatting_suggestions = models.JSONField(default=list)
    keyword_optimization = models.JSONField(default=list)
    ats_score = models.FloatField(null=True, blank=True)
    
    class Meta:
        db_table = 'resume_analyses'
    
    def __str__(self):
        return f"Analysis for {self.resume.title}"

class ResumeFeedback(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='feedback')
    formatting_score = models.FloatField()
    content_score = models.FloatField()
    keyword_score = models.FloatField()
    overall_score = models.FloatField()
    suggestions = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback for {self.resume.title}"

class JobMatch(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='job_matches')
    job = models.ForeignKey('jobs.JobListing', on_delete=models.CASCADE, related_name='resume_matches')
    match_score = models.FloatField()
    skills_match = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('resume', 'job')
        db_table = 'resume_job_matches'
    
    def __str__(self):
        return f"Match: {self.resume.title} - {self.job.title} ({self.match_score}%)" 