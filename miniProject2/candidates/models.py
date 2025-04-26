from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    skills = models.TextField(help_text="Comma-separated list of skills")
    experience = models.IntegerField(help_text="Years of experience")
    education = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.skills}"

    class Meta:
        ordering = ['-created_at']
