from django.db import models

# Create your models here.

class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'profile'
        managed = False  # since it's an existing table in your DB