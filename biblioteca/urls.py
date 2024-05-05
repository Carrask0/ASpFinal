from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bibliotecas/", views.lista_bibliotecas, name="bibliotecas"),
    path("bibliotecas/<int:biblioteca_id>/", views.biblioteca_detail, name="biblioteca_detail"),
    path("libros/", views.lista_libros, name="libros"),
    path("libros/<int:libro_id>/", views.libro_detail, name="libro_detail"),
]