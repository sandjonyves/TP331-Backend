from django.db import models
from account.models import CustomUser
# Create your models here.

class School(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='shool')
    name = models.CharField(max_length=128)
    # devise = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    logo_url = models.CharField(max_length=255)
    # signature = models.ImageField(upload_to='media/schools/signature/', null=True, blank=True)
    academic_year = models.CharField(max_length=128)  # Décommenter si nécessaire
    # name = models.CharField(max_length=128)
    devise = models.CharField(max_length=255,null=True)
    contact = models.CharField(max_length=255,null=True)
    logo = models.TextField(null=True)
    academic_year = models.CharField(max_length=255, null=True, blank=True)
    cachet = models.TextField(null=True)
    signature_principale = models.TextField(null=True)
    
    def __str__(self):
        return self.name
    
    


class Classe(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes',null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Student(models.Model):
    # Relations
    classe = models.ForeignKey(
        'Classe',
        on_delete=models.CASCADE,
        related_name='students'
    )

    matricule = models.CharField(max_length=255, unique=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True)

    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('O', 'Autre'),
    ]
    sexe = models.CharField(
        max_length=10,
        choices=SEXE_CHOICES,
        null=True,
        blank=True
    )
    image_url = models.CharField(
        max_length=254,
        null=True,
        blank=True,
        help_text="Lien vers l'image de l'étudiant."
    )
    photos = models.TextField(
        null=True,
        blank=True,
     
    )
    card_file = models.FileField(
        upload_to='card/',
        null=True,
        blank=True,
        help_text="Fichier PDF de la carte générée."
    )
 
 

    def __str__(self):
        return f"{self.firstName} {self.lastName}" 


class Card(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='carts')  # Correction du related_name
    card_file = models.FileField(upload_to='card/')  

    def __str__(self):
        return self.student.matricule
    

class CardPrototype(models.Model):
    image =models.CharField(max_length=256)
    choice = models.BooleanField(default=False)