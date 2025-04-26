from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ResumeUploadView,
    ResumeAnalysisViewSet,
    JobMatchView,
    ResumeStatsView
)

router = DefaultRouter()
router.register(r'analyses', ResumeAnalysisViewSet, basename='resume-analysis')

urlpatterns = [
    path('', include(router.urls)),
    path('upload/', ResumeUploadView.as_view(), name='resume-upload'),
    path(
        'analyses/<int:resume_analysis_id>/matches/',
        JobMatchView.as_view(),
        name='job-matches'
    ),
    path('stats/', ResumeStatsView.as_view(), name='resume-stats'),
] 