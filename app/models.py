from django.db import models
from account.models import CustomUser

class School(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=128)
    devise = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    logo = models.TextField(null=True)
    academic_year = models.CharField(max_length=255, null=True, blank=True)
    cachet = models.TextField(null=True)
    signature_principale = models.TextField(null=True)

    def __str__(self):
        return self.name




class Classe(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classe')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Student(models.Model):
    classe = models.ForeignKey(Classe,on_delete=models.CASCADE,related_name='students')
    matricule = models.CharField(max_length=255,unique=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    photos = models.TextField(null=True)
  

    def __str__(self):
        return self.firstName


class Cart(models.Model):
    student = models.OneToOneField(Student,on_delete=models.CASCADE,related_name='student')
    image = models.TextField(null=True)

    def __str__(self):
        return self.student.matricule

