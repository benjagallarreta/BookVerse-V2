from django.db import models

# Create your models here.
from django.db import models
from Usuario.models import Usuario
from Pedidos.models import Libro

class Cart(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=None)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, default=None)
    cantidad = models.PositiveIntegerField(default=1) 
    precio = models.DecimalField(max_digits=10, decimal_places=2)