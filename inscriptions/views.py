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
        document_form = DocumentForm()
        
        if candidat_form.is_valid():
            # Sauvegarder le candidat sans attendre la validation des documents
            candidat = candidat_form.save()
            
            # Traiter le fichier ZIP s'il existe
            if 'documents_zip' in request.FILES:
                zip_file = request.FILES['documents_zip']
                
                try:
                    # Créer un dossier temporaire pour extraire les fichiers
                    with tempfile.TemporaryDirectory() as temp_dir:
                        # Extraire le fichier ZIP
                        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                            zip_ref.extractall(temp_dir)
                        
                        # Liste des documents requis
                        required_documents = [field.name for field in document_form]
                        documents_found = []
                        
                        # Parcourir les fichiers extraits du ZIP
                        for root, dirs, files in os.walk(temp_dir):
                            for file in files:
                                # Accepter tous les types de fichiers, pas seulement les PDF
                                base_name = os.path.splitext(file)[0]
                                if base_name in required_documents:
                                    file_path = os.path.join(root, file)
                                    
                                    # Créer un objet Document
                                    with open(file_path, 'rb') as f:
                                        Document.objects.create(
                                            candidat=candidat,
                                            type_document=base_name,
                                            fichier=f
                                        )
                                    
                                    documents_found.append(base_name)
                        
                        # Message de succès même si tous les documents ne sont pas présents
                        if documents_found:
                            messages.success(request, "Votre candidature a été soumise avec succès!")
                        else:
                            messages.warning(request, "Votre candidature a été enregistrée, mais aucun document n'a été trouvé dans l'archive.")
                        
                        return redirect('confirmation', candidat_id=candidat.id)
                
                except Exception as e:
                    # En cas d'erreur, on garde quand même le candidat et on affiche un message
                    messages.warning(request, f"Votre candidature a été enregistrée, mais il y a eu un problème avec vos documents: {str(e)}")
                    return redirect('confirmation', candidat_id=candidat.id)
            else:
                # Même sans fichier ZIP, on accepte la candidature
                messages.warning(request, "Votre candidature a été enregistrée sans documents. Vous pourrez les ajouter ultérieurement.")
                return redirect('confirmation', candidat_id=candidat.id)
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



