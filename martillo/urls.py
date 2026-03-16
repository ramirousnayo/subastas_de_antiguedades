from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.registro, name='registro'),
    path('publicar/', views.publicar_pieza, name='publicar_pieza'),
]
