from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bibliotecas/", views.lista_bibliotecas, name="bibliotecas"),
    path("bibliotecas/<int:biblioteca_id>/", views.biblioteca_detail, name="biblioteca_detail"),
    path("libros/", views.lista_libros, name="libros"),
    path("libros/<int:libro_id>/", views.libro_detail, name="libro_detail"),
    path('bibliotecas/buscar_por_nombre/', views.buscar_biblioteca_nombre, name='buscar_biblioteca_nombre'),
    path('bibliotecas/buscar_por_ciudad/', views.buscar_biblioteca_ciudad, name='buscar_biblioteca_ciudad'),

    ## Functionality routes
    path('delete_libro/<int:libro_id>/', views.delete_libro, name='delete_libro'),
    path('form_edit_libro/<int:libro_id>/', views.form_edit_libro, name='form_edit_libro'),
    path('form_create_libro/', views.form_create_libro, name='form_create_libro'),
]