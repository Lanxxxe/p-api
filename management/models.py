from django.db import models

# Create your models here.
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
        