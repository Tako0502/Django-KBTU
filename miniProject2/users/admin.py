from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, JobSeekerProfile, RecruiterProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'email_verified', 'date_joined')
    list_filter = ('role', 'email_verified', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'email_verified', 'phone_number', 'profile_picture')}),
    )

class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'created_at')
    search_fields = ('user__username', 'user__email', 'location')
    list_filter = ('created_at',)

class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'created_at')
    search_fields = ('user__username', 'user__email', 'company_name')
    list_filter = ('created_at',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(JobSeekerProfile, JobSeekerProfileAdmin)
admin.site.register(RecruiterProfile, RecruiterProfileAdmin) 