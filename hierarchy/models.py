from django.db import models

# Create your models here.
class Designation(models.Model):
    name = models.CharField(max_length=255, unique=True)
    superior = models.CharField(max_length=255)
    juniors = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
