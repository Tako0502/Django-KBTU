from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    JobSeekerProfileView,
    RecruiterProfileView,
    PasswordResetView,
    PasswordResetConfirmView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('job-seeker/profile/', JobSeekerProfileView.as_view(), name='job-seeker-profile'),
    path('recruiter/profile/', RecruiterProfileView.as_view(), name='recruiter-profile'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
] 