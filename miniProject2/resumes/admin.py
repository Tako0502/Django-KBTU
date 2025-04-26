from django.contrib import admin
from .models import Resume, ResumeAnalysis, ResumeFeedback, JobMatch

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'upload_date', 'is_public', 'ai_score')
    list_filter = ('is_public', 'upload_date')
    search_fields = ('title', 'user__email', 'full_name')
    date_hierarchy = 'upload_date'

@admin.register(ResumeAnalysis)
class ResumeAnalysisAdmin(admin.ModelAdmin):
    list_display = ('resume', 'analysis_date', 'ats_score')
    list_filter = ('analysis_date',)
    search_fields = ('resume__title', 'resume__user__email')
    date_hierarchy = 'analysis_date'

@admin.register(ResumeFeedback)
class ResumeFeedbackAdmin(admin.ModelAdmin):
    list_display = ('resume', 'formatting_score', 'content_score', 'keyword_score', 'overall_score', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('resume__title', 'resume__user__email')
    date_hierarchy = 'created_at'

@admin.register(JobMatch)
class JobMatchAdmin(admin.ModelAdmin):
    list_display = ('resume', 'job', 'match_score', 'created_at')
    list_filter = ('match_score', 'created_at')
    search_fields = ('resume__title', 'job__title')
    date_hierarchy = 'created_at' 