from django.db import models
from Home.models import Libro
from Usuario.models import Usuario
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Reseña(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='resenas')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    comentario = models.TextField(blank=True, null=True)
    estrellas = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)
    fecha = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.usuario.username} - {self.libro.titulo} - {self.estrellas} estrellas"