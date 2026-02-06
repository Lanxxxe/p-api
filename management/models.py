from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta


class Manager(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'manager'
        verbose_name = 'Manager'
        verbose_name_plural = 'Managers'
        

class InternshipLog(models.Model):
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField()
    hours = models.FloatField(default=0)  # Auto-calculated, default to 0
    notes = models.TextField()
    photos = models.ImageField(upload_to='internship_photos/', blank=True, null=True)


    def __str__(self):
        return f"{self.date} - {self.hours} hours"
    
    def save(self, *args, **kwargs):
        # Calculate hours based on time_in and time_out
        if self.time_in and self.time_out:

            # Convert time objects to datetime for proper calculation
            today = datetime.today()
            time_in_dt = datetime.combine(today, self.time_in)
            time_out_dt = datetime.combine(today, self.time_out)
            
            # Handle overnight shifts
            if time_out_dt < time_in_dt:
                time_out_dt += timedelta(days=1)
            
            time_diff = time_out_dt - time_in_dt
            total_hours = time_diff.total_seconds() / 3600  # Convert to hours
            
            # Subtract 1 hour for lunch break (12nn - 1pm) if shift spans that time
            lunch_start = datetime.combine(today, datetime.strptime('12:00', '%H:%M').time())
            lunch_end = datetime.combine(today, datetime.strptime('13:00', '%H:%M').time())
            
            # Check if the work period includes lunch break
            if time_in_dt < lunch_end and time_out_dt > lunch_start:
                total_hours -= 1  # Deduct 1 hour for lunch break
            
            self.hours = total_hours
        super().save(*args, **kwargs)


class Achievement(models.Model):
    event = models.CharField(max_length=200)
    ranked = models.CharField(max_length=100)
    summary = models.TextField()
    description = models.TextField()
    location = models.CharField(max_length=200)
    date_achieved = models.DateField()
    proof_url = models.TextField()
    category = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event
    
    class Meta:
        db_table = 'achievements'
        verbose_name = 'Achievement'
        verbose_name_plural = 'Achievements'



class Project(models.Model):
    project_name = models.CharField(max_length=200)
    summary = models.TextField()
    description = models.TextField()
    languages = models.TextField()
    project_image = models.TextField()
    project_url = models.URLField()
    category = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_name
    

    class Meta:
        db_table = 'projects'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'



class Tool(models.Model):
    tool_name = models.CharField(max_length=200)
    description = models.TextField()
    version = models.CharField(max_length=50)
    icon_url = models.TextField()
    category = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tool_name
    

    class Meta:
        db_table = 'tools'
        verbose_name = 'Tool'
        verbose_name_plural = 'Tools'