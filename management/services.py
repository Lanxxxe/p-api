from management.models import InternshipLog, Project, Achievement, Tool
from django.db.models import Sum
from datetime import date, timedelta
from management.serializer import InternshipLogSerializer, ProjectSerializer

class InternshipService:

    @staticmethod
    def calculate_total_hours():
        """Calculate total hours from all logs"""
        total_hours = InternshipLog.objects.aggregate(total=Sum('hours'))['total'] or 0
        return total_hours


    @staticmethod
    def calculate_remaining_hours(total_hours_needed=486):
        """Calculate remaining hours needed"""
        total_hours = InternshipService.calculate_total_hours()
        remaining_hours = max(total_hours_needed - total_hours, 0)
        return remaining_hours

    @staticmethod
    def calculate_remaining_days(remaining_hours, hours_per_day=8):
        """Calculate remaining days based on remaining hours and hours per day"""
        if hours_per_day <= 0:
            return 0
        remaining_days = remaining_hours / hours_per_day
        return max(remaining_days, 0)
 
    @staticmethod
    def calculate_estimated_completion_date(remaining_hours, hours_per_day=8):
        """Calculate estimated completion date based on remaining hours and hours per day"""
        if hours_per_day <= 0:
            return None
        remaining_days = InternshipService.calculate_remaining_days(remaining_hours, hours_per_day)
        estimated_completion_date = date.today() + timedelta(days=remaining_days)
        return estimated_completion_date
    
    @staticmethod
    def create_log(data):
        """Create a new internship log"""
        serializer = InternshipLogSerializer(data=data)
        if not serializer.is_valid():
            raise ValueError(serializer.errors)
        log = serializer.save()
        return log
    

class ProjectService:
    
    @staticmethod
    def get_all_projects():
        """Retrieve all projects"""

        return Project.objects.all()
    
    @staticmethod
    def create_project(data):
        serializer = ProjectSerializer(data=data)
        if not serializer.is_valid():
            raise ValueError(serializer.errors)
        
        # Create project with validated data
        project = Project.objects.create(
            project_name=serializer.validated_data['project_name'],
            summary=serializer.validated_data['summary'],
            description=serializer.validated_data['description'],
            languages=serializer.validated_data['languages'],
            project_url=serializer.validated_data['project_url'],
            project_image=serializer.validated_data.get('project_image', ''),
            category=serializer.validated_data.get('category', [])
        )
        return project




