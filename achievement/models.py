from django.db import models

# Create your models here.
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