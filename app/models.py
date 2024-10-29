from django.db import models

# Create your models here.



class School(models.Model):
    school_name = models.CharField(max_length=128)


    def __str__(self):
        return self.school_name




class Classe(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classe')

    name = models.CharField(max_length=255)


class Student(models.Model):
    classe = models.ForeignKey(Classe,on_delete=models.CASCADE,related_name='students')
    matricule = models.CharField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    grade = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Cart(models.Model):

    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='student')
    image = models.ImageField(upload_to='student/images')


    