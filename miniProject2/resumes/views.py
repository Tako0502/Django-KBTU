from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .models import Resume, ResumeAnalysis, ResumeFeedback, JobMatch
from .serializers import (
    ResumeSerializer,
    ResumeAnalysisSerializer,
    ResumeFeedbackSerializer,
    JobMatchSerializer,
    ResumeUploadSerializer,
    ResumeAnalysisRequestSerializer,
    ResumeFeedbackRequestSerializer,
    JobMatchRequestSerializer,
    ResumeUpdateSerializer
)
from .tasks import process_resume, analyze_resume, generate_feedback, match_job, process_resume_analysis

class ResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Resume.objects.none()
        return Resume.objects.filter(user=self.request.user)
    
    @method_decorator(ratelimit(key='user', rate='10/hour', method='POST'))
    def create(self, request, *args, **kwargs):
        serializer = ResumeUploadSerializer(data=request.data)
        if serializer.is_valid():
            resume = serializer.save(user=request.user)
            # Trigger async analysis
            process_resume_analysis.delay(resume.id)
            return Response(ResumeSerializer(resume).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @method_decorator(ratelimit(key='user', rate='20/hour', method='PUT'))
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ResumeUpdateSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def analysis(self, request, pk=None):
        resume = self.get_object()
        analysis = ResumeAnalysis.objects.filter(resume=resume).first()
        if analysis:
            serializer = ResumeAnalysisSerializer(analysis)
            return Response(serializer.data)
        return Response({'detail': 'No analysis available yet'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def public(self, request):
        public_resumes = Resume.objects.filter(is_public=True)
        serializer = self.get_serializer(public_resumes, many=True)
        return Response(serializer.data)

class ResumeListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        resumes = Resume.objects.filter(user=request.user)
        serializer = ResumeSerializer(resumes, many=True)
        return Response(serializer.data)

class ResumeDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        serializer = ResumeSerializer(resume)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        resume.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ResumeUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        serializer = ResumeUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            resume = Resume.objects.create(
                user=request.user,
                file=file,
                original_filename=file.name,
                file_type=file.name.split('.')[-1].lower()
            )
            # Start background processing
            process_resume.delay(resume.id)
            return Response(ResumeSerializer(resume).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResumeAnalysisView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        analysis = get_object_or_404(ResumeAnalysis, resume=resume)
        serializer = ResumeAnalysisSerializer(analysis)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ResumeAnalysisRequestSerializer(data=request.data)
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
        serializer = ResumeFeedbackRequestSerializer(data=request.data)
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
        serializer = JobMatchRequestSerializer(data=request.data)
        if serializer.is_valid():
            resume = get_object_or_404(Resume, pk=serializer.validated_data['resume_id'], user=request.user)
            # Start background job matching
            match_job.delay(resume.id, serializer.validated_data['job_id'])
            return Response({'message': 'Job matching started'}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 