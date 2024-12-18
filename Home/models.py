from django.db import models


class TipoLibro (models.TextChoices):
        INDEFINIDO = 'Indefinido', 'I' 
        FISICO = 'Libro Fisico', 'F'
        AUDIO =  'Audio Libro', 'A'
        ELECTRONICO = 'Ebook', 'E'

class Libro(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True)
    portada = models.ImageField(blank=True, upload_to='static/portada', null=True, verbose_name='Imagen del libro')
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=False, blank=False)
    titulo = models.CharField(max_length=100, blank=False)
    autor = models.CharField(max_length=100, blank=False)
    sinopsis = models.TextField(blank=False, default='Sinopsis No Disponible')
    editorial = models.CharField(max_length=100, blank=True)
    genero = models.CharField(max_length=100, blank=False)
    cant_paginas = models.PositiveSmallIntegerField(null=True, blank=True)
    dimension = models.CharField(max_length=50, null=True, blank=True)
    encuadernacion = models.CharField(max_length=50, null=True, blank=True)
    tipo = models.CharField(max_length=15, choices=TipoLibro.choices, default=TipoLibro.FISICO)
    narrador = models.CharField(max_length=100, null=True, blank=True)
    duracion = models.SmallIntegerField(null=True, blank=True)
    extension_archivo = models.CharField(max_length=10, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)

    def _str_(self):
        return self.isbn
    
    class Meta:
        permissions = [
            ("can_change_stock", "Can change stock of books"),  # Permiso personalizado
        ]