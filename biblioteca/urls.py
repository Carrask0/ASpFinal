from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bibliotecas/", views.lista_bibliotecas, name="bibliotecas"),
    path("bibliotecas/<int:biblioteca_id>/", views.biblioteca_detail, name="biblioteca_detail"),
]