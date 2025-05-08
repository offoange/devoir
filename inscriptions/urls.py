from django.urls import path
from . import views


urlpatterns = [
    path('', views.inscription, name='inscription'),
    path('confirmation/<int:candidat_id>/', views.confirmation, name='confirmation'),
]