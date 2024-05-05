from django.shortcuts import render
from django.http import HttpResponse
from .models import Biblioteca, Libro
from faker import Faker
import random


# Create your views here.
def index(request):

    

    fake = Faker()
    if Biblioteca.objects.all().count() == 0:
        # Populate Biblioteca table
        for _ in range(10):
            nombre = fake.company()
            direccion = fake.address()
            ciudad = fake.city()
            horario_apertura = fake.time(pattern='%H:%M:%S')
            horario_cierre = fake.time(pattern='%H:%M:%S')
            fecha_fundacion = fake.date_this_century()
            normas = None  # You can add mock file paths here
            Biblioteca.objects.create(nombre=nombre, direccion=direccion, ciudad=ciudad,
                                        horario_apertura=horario_apertura, horario_cierre=horario_cierre,
                                        fecha_fundacion=fecha_fundacion, normas=normas)

    if Libro.objects.all().count() == 0:
        # Populate Libro table
        bibliotecas = Biblioteca.objects.all()
        for _ in range(50):
            titulo = fake.catch_phrase()
            autor = fake.name()
            sinopsis = fake.text()
            anio_publicacion = fake.date_this_century()
            editorial = fake.company()
            isbn = fake.isbn13()
            num_ejemplares = random.randint(1, 10)
            biblioteca = random.choice(bibliotecas)
            Libro.objects.create(titulo=titulo, autor=autor, sinopsis=sinopsis,
                                 anio_publicacion=anio_publicacion, editorial=editorial, isbn=isbn,
                                 num_ejemplares=num_ejemplares, biblioteca=biblioteca)

    return HttpResponse("Base de datos poblada con datos de prueba")

def lista_bibliotecas(request):
    bibliotecas = Biblioteca.objects.all()
    return render(request, "lista_bibliotecas.html", {"bibliotecas": bibliotecas})

def biblioteca_detail(request, biblioteca_id):
    biblioteca = Biblioteca.objects.get(pk=biblioteca_id)
    libros = Libro.objects.filter(biblioteca=biblioteca)
    return render(request, "biblioteca_detail.html", {"biblioteca": biblioteca, "libros": libros})

