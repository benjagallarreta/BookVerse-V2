from django.db import models
from Pedidos.models import Libro
from Usuario.models import Usuario


class WishList(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=None)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, default=None)
    agregado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'libro')

    def _str_(self):
        return f"{self.usuario.username} - {self.libro.titulo}"