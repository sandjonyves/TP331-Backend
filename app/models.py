from django.db import models
# from app.models import Student

# Create your models here.



class School(models.Model):
    name = models.CharField(max_length=128)
    devise = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    logo = models.TextField()
    # academic_year = models.DateField()

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
  

    def __str__(self):
        return self.firstName


class Cart(models.Model):

    student = models.OneToOneField(Student,on_delete=models.CASCADE,related_name='student')
    image = models.TextField()

    def __str__(self):
        return self.student.matricule

