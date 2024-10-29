from django.db import models

# Create your models here.

class School(models.Model):
    school_name = models.CharField(max_length=128)



# class 