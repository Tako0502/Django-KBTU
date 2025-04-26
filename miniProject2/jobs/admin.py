from django.contrib import admin
from .models import JobListing, JobApplication, JobCategory, JobCategoryMapping, JobMatch

@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'job_type', 'posted_by', 'posted_date', 'is_active')
    list_filter = ('job_type', 'is_active', 'posted_date')
    search_fields = ('title', 'company', 'location', 'description')
    date_hierarchy = 'posted_date'

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'applied_date', 'match_score')
    list_filter = ('status', 'applied_date')
    search_fields = ('job__title', 'applicant__email')
    date_hierarchy = 'applied_date'

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(JobCategoryMapping)
class JobCategoryMappingAdmin(admin.ModelAdmin):
    list_display = ('job', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('job__title', 'category__name')

@admin.register(JobMatch)
class JobMatchAdmin(admin.ModelAdmin):
    list_display = ('job', 'resume', 'match_score', 'created_at')
    list_filter = ('match_score', 'created_at')
    search_fields = ('job__title', 'resume__title')
    date_hierarchy = 'created_at' 