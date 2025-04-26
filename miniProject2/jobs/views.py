from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from django.utils import timezone
from .models import JobListing, JobApplication, JobMatch
from .serializers import (
    JobListingSerializer,
    JobApplicationSerializer,
    JobMatchSerializer,
    JobApplicationCreateSerializer
)
from .tasks import calculate_job_match

class JobListingFilter(filters.FilterSet):
    min_salary = filters.NumberFilter(field_name="salary_min", lookup_expr='gte')
    max_salary = filters.NumberFilter(field_name="salary_max", lookup_expr='lte')
    job_type = filters.CharFilter(field_name="job_type")
    location = filters.CharFilter(field_name="location", lookup_expr='icontains')
    company = filters.CharFilter(field_name="company", lookup_expr='icontains')
    
    class Meta:
        model = JobListing
        fields = ['job_type', 'location', 'company', 'min_salary', 'max_salary']

class JobListingViewSet(viewsets.ModelViewSet):
    serializer_class = JobListingSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = JobListingFilter
    
    def get_queryset(self):
        queryset = JobListing.objects.filter(is_active=True, expiry_date__gt=timezone.now())
        if self.action == 'my_jobs':
            return queryset.filter(posted_by=self.request.user)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_jobs(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        job = self.get_object()
        serializer = JobApplicationCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            application = serializer.save(
                job=job,
                applicant=request.user
            )
            calculate_job_match.delay(application.id)
            return Response(
                JobApplicationSerializer(application).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.action == 'my_applications':
            return JobApplication.objects.filter(applicant=self.request.user)
        elif self.action == 'job_applications':
            job_id = self.kwargs.get('job_pk')
            return JobApplication.objects.filter(job_id=job_id)
        return JobApplication.objects.none()
    
    @action(detail=False, methods=['get'])
    def my_applications(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='job/(?P<job_pk>[^/.]+)')
    def job_applications(self, request, job_pk=None):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class JobMatchViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobMatchSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.action == 'resume_matches':
            resume_id = self.kwargs.get('resume_pk')
            return JobMatch.objects.filter(resume_id=resume_id)
        elif self.action == 'job_matches':
            job_id = self.kwargs.get('job_pk')
            return JobMatch.objects.filter(job_id=job_id)
        return JobMatch.objects.none()
    
    @action(detail=False, methods=['get'], url_path='resume/(?P<resume_pk>[^/.]+)')
    def resume_matches(self, request, resume_pk=None):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='job/(?P<job_pk>[^/.]+)')
    def job_matches(self, request, job_pk=None):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data) 