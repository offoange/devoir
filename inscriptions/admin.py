from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Candidat, Document

@admin.register(Candidat)
class CandidatAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenoms', 'email', 'concours_souhaite')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('candidat', 'type_document')