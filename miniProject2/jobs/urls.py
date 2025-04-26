from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobListingViewSet, JobApplicationViewSet, JobMatchViewSet

router = DefaultRouter()
router.register(r'listings', JobListingViewSet, basename='job-listing')
router.register(r'applications', JobApplicationViewSet, basename='job-application')
router.register(r'matches', JobMatchViewSet, basename='job-match')

urlpatterns = [
    path('', include(router.urls)),
] 