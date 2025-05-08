from django.shortcuts import render, redirect
from django.contrib import messages
import zipfile
import os
import tempfile
from .models import Candidat, Document
from .forms import CandidatForm, DocumentForm

def accueil(request):
    return render(request, 'inscriptions/accueil.html')

def inscription(request):
    if request.method == 'POST':
        candidat_form = CandidatForm(request.POST)
        document_form = DocumentForm()  # Pas de données POST nécessaire pour ce formulaire
        
        if candidat_form.is_valid():
            # Vérifier si un fichier ZIP a été fourni
            if 'documents_zip' in request.FILES:
                zip_file = request.FILES['documents_zip']
                
                # Sauvegarder le candidat
                candidat = candidat_form.save()
                
                # Créer un dossier temporaire pour extraire les fichiers ZIP
                with tempfile.TemporaryDirectory() as temp_dir:
                    # Extraire le fichier ZIP
                    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                        zip_ref.extractall(temp_dir)
                    
                    # Vérifier les documents requis
                    required_documents = [field.name for field in document_form]
                    documents_found = []
                    
                    # Parcourir les fichiers extraits du ZIP
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            for doc_type in required_documents:
                                if file.startswith(doc_type) and file.lower().endswith('.pdf'):
                                    file_path = os.path.join(root, file)
                                    
                                    # Ouvrir le fichier
                                    with open(file_path, 'rb') as f:
                                        # Créer un objet Document
                                        Document.objects.create(
                                            candidat=candidat,
                                            type_document=doc_type,
                                            fichier=f  # Django gère automatiquement l'enregistrement du fichier
                                        )
                                    
                                    documents_found.append(doc_type)
                    
                    # Vérifier si tous les documents requis ont été fournis
                    if set(documents_found) == set(required_documents):
                        messages.success(request, "Votre candidature a été soumise avec succès!")
                        return redirect('confirmation', candidat_id=candidat.id)
                    else:
                        # Supprimer le candidat et afficher une erreur
                        candidat.delete()
                        missing_docs = set(required_documents) - set(documents_found)
                        messages.error(request, f"Documents manquants: {', '.join(missing_docs)}. Veuillez réessayer.")
            else:
                messages.error(request, "Veuillez téléverser une archive ZIP contenant tous les documents requis.")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    
    else:
        candidat_form = CandidatForm()
        document_form = DocumentForm()
    
    return render(request, 'inscriptions/inscription.html', {
        'candidat_form': candidat_form,
        'document_form': document_form,
    })

def confirmation(request, candidat_id):
    try:
        candidat = Candidat.objects.get(id=candidat_id)
        documents = Document.objects.filter(candidat=candidat)
        
        return render(request, 'inscriptions/confirmation.html', {
            'candidat': candidat,
            'documents': documents
        })
    except Candidat.DoesNotExist:
        messages.error(request, "Candidature introuvable.")
        return redirect('inscription')



