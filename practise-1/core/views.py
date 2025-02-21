import logging
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Project, Category, Priority, Task
from .serializers import (
    UserSerializer, ProjectSerializer, CategorySerializer,
    PrioritySerializer, TaskSerializer
)
from .permissions import IsAdmin, IsManager, IsEmployee, IsTaskAssignee

logger = logging.getLogger(__name__)

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsManager]

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsManager]

class PriorityViewSet(ModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer
    permission_classes = [IsManager]

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsEmployee]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['project', 'priority', 'category']
    search_fields = ['title', 'description']

    def get_queryset(self):
        if self.request.user.role == 'employee':
            return Task.objects.filter(assignee=self.request.user)
        return Task.objects.all()

    def perform_create(self, serializer):
        logger.info(f"Creating a new task by user {self.request.user}")
        serializer.save() 