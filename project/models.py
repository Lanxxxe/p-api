from django.db import models

# Create your models here.
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