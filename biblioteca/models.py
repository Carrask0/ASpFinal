from django.db import models

class Biblioteca(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, help_text="Debe contener un número al final")
    ciudad = models.CharField(max_length=100)
    horario_apertura = models.TimeField()
    horario_cierre = models.TimeField()
    fecha_fundacion = models.DateField()
    normas = models.FileField(upload_to='normas/', null=True, blank=True)

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    sinopsis = models.TextField()
    anio_publicacion = models.DateField()
    editorial = models.CharField(max_length=100)
    isbn = models.CharField(max_length=17, help_text="Formato: 0-7645-2641-3")
    num_ejemplares = models.IntegerField()
    biblioteca = models.ForeignKey(Biblioteca, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo
