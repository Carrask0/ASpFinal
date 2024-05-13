from .models import Biblioteca, Libro

class RepositoryService:
    def __init__ (self):
        self.bibliotecas = Biblioteca.objects.all()
        self.libros = Libro.objects.all()

    def get_bibliotecas(self):
        return self.bibliotecas
    
    def get_libros(self):
        return self.libros
    
    def get_biblioteca(self, biblioteca_id):
        return Biblioteca.objects.get(id=biblioteca_id)
    
    def get_libro(self, libro_id):
        return Libro.objects.get(id=libro_id)
    
    def delete_libro(self, libro_id):
        Libro.objects.get(id=libro_id).delete()

    def delete_biblioteca(self, biblioteca_id):
        Biblioteca.objects.get(id=biblioteca_id).delete()

    def create_libro(self, titulo, autor, sinopsis, anio_publicacion, editorial, num_ejemplares, biblioteca):
        libro = Libro(titulo=titulo, autor=autor, sinopsis=sinopsis, anio_publicacion=anio_publicacion, editorial=editorial, num_ejemplares=num_ejemplares, biblioteca=biblioteca)
        libro.save()

    def create_biblioteca(self, nombre, direccion, ciudad, horario_apertura, horario_cierre, fecha_fundacion, normas = None):
        biblioteca = Biblioteca(nombre=nombre, direccion=direccion, ciudad=ciudad, horario_apertura=horario_apertura, horario_cierre=horario_cierre, fecha_fundacion=fecha_fundacion, normas=normas)
        biblioteca.save()

    def edit_libro(self, libro_id, titulo, autor, sinopsis, anio_publicacion, editorial, num_ejemplares, biblioteca):
        libro = Libro.objects.get(id=libro_id)
        libro.titulo = titulo
        libro.autor = autor
        libro.sinopsis = sinopsis
        libro.anio_publicacion = anio_publicacion
        libro.editorial = editorial
        libro.num_ejemplares = num_ejemplares
        libro.biblioteca = biblioteca
        libro.save()

    def edit_biblioteca(self, biblioteca_id, nombre, direccion, ciudad, horario_apertura, horario_cierre, fecha_fundacion, normas = None):
        biblioteca = Biblioteca.objects.get(id=biblioteca_id)
        biblioteca.nombre = nombre
        biblioteca.direccion = direccion
        biblioteca.ciudad = ciudad
        biblioteca.horario_apertura = horario_apertura
        biblioteca.horario_cierre = horario_cierre
        biblioteca.fecha_fundacion = fecha_fundacion
        biblioteca.normas = normas
        biblioteca.save()

