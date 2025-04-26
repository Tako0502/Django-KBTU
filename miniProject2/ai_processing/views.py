from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_ratelimit.decorators import ratelimit
from .tasks import analyze_resume, generate_feedback, match_jobs
from resumes.models import Resume, ResumeAnalysis, ResumeFeedback
from jobs.models import JobListing
from .models import JobMatch
from .services import match_resume_with_job
from .serializers import (
    ResumeAnalysisSerializer,
    ResumeFeedbackSerializer,
    JobMatchSerializer,
    AnalysisRequestSerializer,
    FeedbackRequestSerializer,
    MatchRequestSerializer,
    ResumeUploadSerializer,
    ResumeAnalysisRequestSerializer
)
from django.utils import timezone

class ResumeAnalysisView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        analysis = get_object_or_404(ResumeAnalysis, resume=resume)
        serializer = ResumeAnalysisSerializer(analysis)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = AnalysisRequestSerializer(data=request.data)
        if serializer.is_valid():
            resume = get_object_or_404(Resume, pk=serializer.validated_data['resume_id'], user=request.user)
            # Start background analysis
            analyze_resume.delay(resume.id)
            return Response({'message': 'Analysis started'}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResumeFeedbackView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        feedback = get_object_or_404(ResumeFeedback, resume=resume)
        serializer = ResumeFeedbackSerializer(feedback)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = FeedbackRequestSerializer(data=request.data)
        if serializer.is_valid():
            resume = get_object_or_404(Resume, pk=serializer.validated_data['resume_id'], user=request.user)
            # Start background feedback generation
            generate_feedback.delay(resume.id)
            return Response({'message': 'Feedback generation started'}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobMatchView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        matches = JobMatch.objects.filter(resume=resume)
        serializer = JobMatchSerializer(matches, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = MatchRequestSerializer(data=request.data)
        if serializer.is_valid():
            resume = get_object_or_404(Resume, pk=serializer.validated_data['resume_id'], user=request.user)
            # Start background job matching
            match_jobs.delay(resume.id)
            return Response({'message': 'Job matching started'}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResumeUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    
    @method_decorator(ratelimit(key='user', rate='10/h', method=['POST']))
    def post(self, request):
        serializer = ResumeUploadSerializer(data=request.data)
        if serializer.is_valid():
            resume_analysis = serializer.save(user=request.user)
            # Start async analysis
            analyze_resume.delay(resume_analysis.id)
            return Response({
                'message': 'Resume uploaded successfully',
                'analysis_id': resume_analysis.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResumeAnalysisViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeAnalysisSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ResumeAnalysis.objects.none()
        return ResumeAnalysis.objects.filter(resume__user=self.request.user)
    
    @method_decorator(ratelimit(key='user', rate='5/hour', method='POST'))
    def create(self, request, *args, **kwargs):
        serializer = ResumeAnalysisRequestSerializer(data=request.data)
        if serializer.is_valid():
            resume = serializer.validated_data['resume']
            if resume.user != request.user:
                return Response(
                    {'detail': 'You do not have permission to analyze this resume'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            analysis = ResumeAnalysis.objects.create(
                resume=resume,
                analysis_date=timezone.now()
            )
            
            # Start background processing
            analyze_resume.delay(analysis.id)
            
            return Response(
                ResumeAnalysisSerializer(analysis).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobMatchView(APIView):
    permission_classes = [IsAuthenticated]
    
    @method_decorator(ratelimit(key='user', rate='50/h', method=['POST']))
    def post(self, request, resume_analysis_id):
        try:
            resume_analysis = ResumeAnalysis.objects.get(
                id=resume_analysis_id,
                user=request.user
            )
        except ResumeAnalysis.DoesNotExist:
            return Response(
                {'error': 'Resume analysis not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        job_description = request.data.get('job_description')
        if not job_description:
            return Response(
                {'error': 'Job description is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Start async job matching
        job_match_id = match_resume_with_job.delay(
            resume_analysis.id,
            job_description
        )
        
        return Response({
            'message': 'Job matching started',
            'job_match_id': str(job_match_id)
        })
    
    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    def get(self, request, resume_analysis_id):
        job_matches = JobMatch.objects.filter(
            resume_analysis_id=resume_analysis_id,
            resume_analysis__user=request.user
        )
        serializer = JobMatchSerializer(job_matches, many=True)
        return Response(serializer.data)

class ResumeStatsView(APIView):
    permission_classes = [IsAuthenticated]
    
    @method_decorator(cache_page(60 * 30))  # Cache for 30 minutes
    def get(self, request):
        cache_key = f'resume_stats_{request.user.id}'
        stats = cache.get(cache_key)
        
        if not stats:
            analyses = ResumeAnalysis.objects.filter(user=request.user)
            stats = {
                'total_resumes': analyses.count(),
                'average_score': analyses.aggregate(Avg('overall_score'))['overall_score__avg'] or 0,
                'total_job_matches': JobMatch.objects.filter(
                    resume_analysis__user=request.user
                ).count()
            }
            cache.set(cache_key, stats, 60 * 30)  # Cache for 30 minutes
        
        return Response(stats) 