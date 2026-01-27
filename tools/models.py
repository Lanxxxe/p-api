from django.db import models

# Create your models here.
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
        

