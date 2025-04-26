from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Candidate
from .serializers import CandidateSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['experience']
    search_fields = ['skills', 'education', 'user__first_name', 'user__last_name']

    def get_queryset(self):
        queryset = super().get_queryset()
        skills = self.request.query_params.get('skills', None)
        if skills:
            skills_list = [skill.strip() for skill in skills.split(',')]
            for skill in skills_list:
                queryset = queryset.filter(skills__icontains=skill)
        return queryset
