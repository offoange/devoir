
from django.contrib import admin
from django.urls import path, include  # Ajoutez 'include' ici
from django.conf import settings
from django.conf.urls.static import static
from inscriptions import views  # importer les vues si tu veux une vue d'accueil




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accueil, name='accueil'),  # Vue d'accueil ici
    path('formulaire/', include('inscriptions.urls')),  # Inclusion des URLs de l'app
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)