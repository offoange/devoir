from django.db import models

# Create your models here.
from django.db import models

class Candidat(models.Model):
    DOCUMENT_TYPES = [
        ('DATE_NAISSANCE', 'Extrait de naissance'),
        ('DIPLOME', 'Diplôme'),
        ('CERTIFICAT', 'Certificat'),
        ('MOTIVATION', 'Lettre de motivation'),
        ('PHOTO', 'Photo'),
    ]
    
    nom = models.CharField(max_length=100)
    prenoms = models.CharField(max_length=100)
    niveau_etudes = models.CharField(max_length=100)
    etablissement_origine = models.CharField(max_length=200)
    concours_souhaite = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=15)
    date_inscription = models.DateTimeField(auto_now_add=True)

class Document(models.Model):
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE, related_name='documents')
    type_document = models.CharField(max_length=50)
    fichier = models.FileField(upload_to='documents/')
    date_upload = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.type_document} pour {self.candidat}"