from django.db import models

# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=128)
    # devise = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    logo_url = models.CharField(max_length=255)
    # signature = models.ImageField(upload_to='media/schools/signature/', null=True, blank=True)
    academic_year = models.CharField(max_length=128)  # Décommenter si nécessaire

    def __str__(self):
        return self.name
    
    


class Classe(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Student(models.Model):
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='students')
    matricule = models.CharField(max_length=255, unique=True)
    firstName = models.CharField(max_length=255)  
    lastName = models.CharField(max_length=255)   
    date_of_birth = models.DateField()
    sexe = models.CharField(max_length=10)  
    image_url = models.CharField(max_length=254)
    # image = models.ImageField(upload_to='students/')

    def __str__(self):
        return f"{self.firstName} {self.lastName}" 


class Cart(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='carts')  # Correction du related_name
    cart_file = models.FileField(upload_to='card/')  

    def __str__(self):
        return self.student.matricule
    

class CardPrototype(models.Model):
    image =models.CharField(max_length=256)
    choice = models.BooleanField(default=False)