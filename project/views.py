from rest_framework import viewsets
from project.serializers import ProjectSerializer
from project.models import Project


# Create your views here.
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer




