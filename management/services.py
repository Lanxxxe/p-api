from management.models import InternshipLog, Project, Achievement, Tool, Manager
from django.db.models import Sum
from datetime import date, timedelta
from management.serializer import InternshipLogSerializer, ProjectSerializer

class InternshipService:

    @staticmethod
    def calculate_total_hours(manager_id=None):
        """Calculate total hours from logs scoped to a manager"""
        qs = InternshipLog.objects.filter(manager_id=manager_id) if manager_id else InternshipLog.objects.none()
        total_hours = qs.aggregate(total=Sum('hours'))['total'] or 0
        return total_hours


    @staticmethod
    def calculate_remaining_hours(total_hours_needed=486, manager_id=None):
        """Calculate remaining hours needed"""
        total_hours = InternshipService.calculate_total_hours(manager_id=manager_id)
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
        """Calculate estimated completion date based on remaining hours and hours per day (excluding weekends)"""
        if hours_per_day <= 0:
            return None
        
        remaining_days = InternshipService.calculate_remaining_days(remaining_hours, hours_per_day)
        
        # Convert to integer days (round up)
        days_to_add = int(remaining_days) if remaining_days == int(remaining_days) else int(remaining_days) + 1
        
        # Start from today
        current_date = date.today()
        weekdays_added = 0
        
        # Add only weekdays (Monday=0 to Friday=4)
        while weekdays_added < days_to_add:
            current_date += timedelta(days=1)
            # Skip weekends (Saturday=5, Sunday=6)
            if current_date.weekday() < 5:
                weekdays_added += 1
        
        return current_date
    
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
    def get_all_projects(manager=None):
        """Retrieve projects scoped to a manager"""
        if manager is not None:
            return Project.objects.filter(manager=manager)
        return Project.objects.none()
    
    @staticmethod
    def create_project(data, manager=None):
        serializer = ProjectSerializer(data=data)
        if not serializer.is_valid():
            raise ValueError(serializer.errors)
        
        project = Project.objects.create(
            manager=manager,
            project_name=serializer.validated_data['project_name'],
            summary=serializer.validated_data['summary'],
            description=serializer.validated_data['description'],
            languages=serializer.validated_data['languages'],
            project_url=serializer.validated_data['project_url'],
            project_image=serializer.validated_data.get('project_image', ''),
            category=serializer.validated_data.get('category', [])
        )
        return project


class ProfileService:

    @staticmethod
    def get_internship_info(manager_id=None):
        """Return internship-related profile fields for the given manager."""
        if not manager_id:
            return None
        manager = Manager.objects.filter(id=manager_id).only(
            'internship_role', 'company', 'school', 'course',
            'total_hours_needed', 'internship_start_date'
        ).first()
        if not manager:
            return None
        return {
            'internship_role': manager.internship_role,
            'company': manager.company,
            'school': manager.school,
            'course': manager.course,
            'total_hours_needed': manager.total_hours_needed,
            'internship_start_date': manager.internship_start_date,
        }


class WeeklyNotesService:

    @staticmethod
    def get_weekly_notes(manager_id=None, week_start=None):
        """
        Return a list of dicts with 'day' and 'notes' for each log
        within the 7-day week starting on week_start (defaults to
        the current Monday).  Only logs that have non-empty notes
        are included.

        Each item:  {'day': date, 'day_name': str, 'notes': str}
        """
        if week_start is None:
            today = date.today()
            week_start = today - timedelta(days=today.weekday())  # Monday

        week_end = week_start + timedelta(days=6)  # Sunday

        qs = (
            InternshipLog.objects
            .filter(
                manager_id=manager_id,
                date__gte=week_start,
                date__lte=week_end,
            )
            .exclude(notes='')
            .order_by('date')
            .values('date', 'notes')
        ) if manager_id else []

        return [
            {
                'day': entry['date'],
                'day_name': entry['date'].strftime('%A'),
                'notes': entry['notes'],
            }
            for entry in qs
        ]

    @staticmethod
    def get_daily_note(manager_id=None, day=None):
        """
        Return the note for a specific day.

        Parameters:
            manager_id: the manager's ID
            day: a date object (defaults to today)

        Returns a dict {'day': date, 'day_name': str, 'notes': str}
        or None if no log exists for that day.
        """
        if day is None:
            day = date.today()

        log = (
            InternshipLog.objects
            .filter(manager_id=manager_id, date=day)
            .values('date', 'notes')
            .first()
        ) if manager_id else None

        if not log:
            return None

        return {
            'day': log['date'],
            'day_name': log['date'].strftime('%A'),
            'notes': log['notes'],
        }

