from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from faker import Faker
import random

from .forms import LibroForm, BibliotecaForm
from .models import Biblioteca, Libro

from .service import RepositoryService

repository = RepositoryService()



# Create your views here.
def index(request):

    NUM_BIBLIOTECAS = 10
    NUM_LIBROS = 50

    #Delete all data from the database
    Libro.objects.all().delete()
    Biblioteca.objects.all().delete()

    #INPUT MOCK DATA
    fake = Faker()
    if Biblioteca.objects.all().count() == 0:
        # Populate Biblioteca table
        for _ in range(NUM_BIBLIOTECAS):
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
        for _ in range(NUM_LIBROS):
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
    """
    Retrieves a list of all libraries from the database and renders them in a template.
    Handles form submissions for searching by library name and city.

    Parameters:
    - request: An HttpRequest object representing the request made by the user.

    Returns:
    - An HttpResponse object representing the rendered HTML page displaying all libraries.
    """
    # Retrieve all libraries by default
    #bibliotecas = Biblioteca.objects.all()
    bibliotecas = repository.get_bibliotecas()

    # Initialize nombre and ciudad to None
    nombre = None
    ciudad = None

    # Check if the request is POST request and process form submissions
    if request.method == 'POST':
        # Check if the form for searching by library name is submitted
        if 'nombre' in request.POST or 'ciudad' in request.POST:
            nombre = request.POST.get('nombre', '')
            ciudad = request.POST.get('ciudad', '')

            # Filter libraries by name and city
            bibliotecas = bibliotecas.filter(nombre__icontains=nombre, ciudad__icontains=ciudad)


    # Render the template with the filtered or all libraries, and pass nombre and ciudad
    return render(request, "lista_bibliotecas.html", {"bibliotecas": bibliotecas, "nombre": nombre, "ciudad": ciudad})



def lista_libros(request):
    """
    Retrieves a list of all books from the database and renders them in a template.
    Handles form submissions for searching libros by titulo.

    Parameters:
    - request: An HttpRequest object representing the request made by the user.

    Returns:
    - An HttpResponse object representing the rendered HTML page displaying all books.
    """
    libros = repository.get_libros()

    # Initialize titulo to None
    titulo = None

    # Check if the request is a POST request and process form submissions
    if request.method == 'POST' and 'titulo' in request.POST:
        titulo = request.POST['titulo']
        # Filter libros by titulo
        libros = libros.filter(titulo__icontains=titulo)


    return render(request, "lista_libros.html", {"libros": libros, "titulo": titulo})


def biblioteca_detail(request, biblioteca_id):
    """
    Retrieves details of a specific library and the books it contains from the database and renders them in a template.
    Handles form submissions for searching libros by titulo, autor, and editorial.

    Parameters:
    - request: An HttpRequest object representing the request made by the user.
    - biblioteca_id: An integer representing the ID of the library.

    Returns:
    - An HttpResponse object representing the rendered HTML page displaying the details of the specified library and the books it contains.
    """
    # Retrieve the biblioteca object by its ID or return a 404 error if it doesn't exist
    biblioteca = repository.get_biblioteca(biblioteca_id)

    # Retrieve all libros associated with the biblioteca
    libros = biblioteca.libro_set.all()

    # Initialize search criteria to empty strings
    titulo = None
    autor = None
    editorial = None

    # Check if the request is a POST request and process form submissions
    if request.method == 'POST':
        # Check if the form for searching libros is submitted
        if 'titulo' in request.POST or 'autor' in request.POST or 'editorial' in request.POST:
            titulo = request.POST.get('titulo', '')
            autor = request.POST.get('autor', '')
            editorial = request.POST.get('editorial', '')

            # Filter libros based on search criteria
            libros = libros.filter(titulo__icontains=titulo, autor__icontains=autor, editorial__icontains=editorial)

    return render(request, "biblioteca_detail.html", {"biblioteca": biblioteca, "libros": libros, "titulo": titulo, "autor": autor, "editorial": editorial})


def libro_detail(request, libro_id):
    """
    Retrieves details of a specific book from the database and renders them in a template.

    Parameters:
    - request: An HttpRequest object representing the request made by the user.
    - libro_id: An integer representing the ID of the book.

    Returns:
    - An HttpResponse object representing the rendered HTML page displaying the details of the specified book.
    """
    libro = repository.get_libro(libro_id)
    return render(request, "libro_detail.html", {"libro": libro})

def delete_libro(request, libro_id):
    """
    Deletes a specific book from the database.

    Parameters:
    - request: An HttpRequest object representing the request made by the user.
    - libro_id: An integer representing the ID of the book to delete.

    Returns:
    - An HttpResponse object indicating the result of the operation.
    """
    libro = repository.get_libro(libro_id)
    libro.delete()


    # Redirect to biblioteca_detail view
    return HttpResponseRedirect("/bibliotecas/" + str(libro.biblioteca.id) + "/")

def form_edit_libro(request, libro_id):
    """
    Displays a form to edit a specific book or updates the book in the database.

    Parameters:
    - request: An HttpRequest object representing the request made by the user.
    - libro_id: An integer representing the ID of the book to edit.

    Returns:
    - An HttpResponse object indicating the result of the operation.
    """
    libro = repository.get_libro(libro_id)
    if request.method == 'POST':
        # If the form is submitted
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()  # Save the form data to update the Libro object
            biblioteca_id = libro.biblioteca.id
            return HttpResponseRedirect("/bibliotecas/" + str(biblioteca_id) + "/")
    else:
        # If it's a GET request, display the form
        form = LibroForm(instance=libro)
        bibliotecas = repository.get_bibliotecas()
    return render(request, "form_libro.html", {"libro": libro, "bibliotecas": bibliotecas})

def form_create_libro(request):
    """
    Displays a form to create a new book or creates a new book in the database.

    Parameters:
    - request: An HttpRequest object representing the request made by the user.

    Returns:
    - An HttpResponse object indicating the result of the operation.
    """
    if request.method == 'POST':
        # If the form is submitted
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to create a new Libro object
            biblioteca_id = form.cleaned_data['biblioteca'].id
            return HttpResponseRedirect("/bibliotecas/" + str(biblioteca_id) + "/")
    else:
        # If it's a GET request, display the form
        form = LibroForm()
        bibliotecas = repository.get_bibliotecas()
    return render(request, "form_libro.html", {"bibliotecas": bibliotecas})


def form_create_biblioteca(request):
    if request.method == 'POST':
        form = BibliotecaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/bibliotecas/")
    else:
        form = BibliotecaForm()
    return render(request, 'form_biblioteca.html', {'form': form})

def form_edit_biblioteca(request, biblioteca_id):
    biblioteca = repository.get_biblioteca(biblioteca_id)
    if request.method == 'POST':
        form = BibliotecaForm(request.POST, instance=biblioteca)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/bibliotecas/")
    else:
        form = BibliotecaForm(instance=biblioteca)
    return render(request, 'form_biblioteca.html', {'form': form, 'biblioteca': biblioteca})


def delete_biblioteca(request, biblioteca_id):
    """
    Deletes a specific library from the database.

    Parameters:
    - request: An HttpRequest object representing the request made by the user.
    - biblioteca_id: An integer representing the ID of the library to delete.

    Returns:
    - An HttpResponse object indicating the result of the operation.
    """
    print("Deleting biblioteca")
    biblioteca = repository.get_biblioteca(biblioteca_id)
    biblioteca.delete()

    # Redirect to lista_bibliotecas view
    return HttpResponseRedirect("/bibliotecas/")

        


    

