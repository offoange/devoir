from django import forms
from .models import Candidat

class CandidatForm(forms.ModelForm):
    class Meta:
        model = Candidat
        fields = '__all__'

class DocumentForm(forms.Form):  # Utilisez Form au lieu de ModelForm
    TYPE_DOCUMENT_CHOICES = [
        ('BIRTH', 'Extrait de naissance'),
        ('DIPLOME', 'Diplôme'),
        ('CERTIFICAT', 'Certificat'),
        ('MOTIVATION', 'Lettre de motivation'),
        ('PHOTO', 'Photo'),
    ]
    
    type_document = forms.ChoiceField(choices=TYPE_DOCUMENT_CHOICES)
    fichiers = forms.FileField()