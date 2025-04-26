from django.db import models
from django.conf import settings
from django.utils import timezone
from users.models import User

class JobListing(models.Model):
    JOB_TYPES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    )
    
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    description = models.TextField()
    requirements = models.JSONField(default=list)
    skills = models.JSONField(default=list)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    posted_date = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-posted_date']
        db_table = 'job_listings'
    
    def __str__(self):
        return f"{self.title} at {self.company}"

class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('reviewing', 'Reviewing'),
        ('shortlisted', 'Shortlisted'),
        ('interviewing', 'Interviewing'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    )
    
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resume = models.ForeignKey('resumes.Resume', on_delete=models.CASCADE)
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_date = models.DateTimeField(default=timezone.now)
    match_score = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['-applied_date']
        db_table = 'job_applications'
        unique_together = ('job', 'applicant', 'resume')
    
    def __str__(self):
        return f"{self.applicant.email} - {self.job.title}"

class JobMatch(models.Model):
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    resume = models.ForeignKey('resumes.Resume', on_delete=models.CASCADE)
    match_score = models.FloatField()
    skills_match = models.JSONField(default=list)
    requirements_match = models.JSONField(default=list)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-match_score']
        db_table = 'job_matches'
        unique_together = ('job', 'resume')
    
    def __str__(self):
        return f"Match: {self.resume.title} - {self.job.title} ({self.match_score}%)"

class JobCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class JobCategoryMapping(models.Model):
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, related_name='jobs')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('job', 'category')
    
    def __str__(self):
        return f"{self.job.title} - {self.category.name}" 