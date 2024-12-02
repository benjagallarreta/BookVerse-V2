# models.py en la aplicación pedidos
import uuid
from django.db import models
from Usuario.models import Usuario


class EstadoPedido(models.TextChoices):  # Define los diferentes estados que puede tomar un pedido
    PENDIENTE = 'Pendiente', 'P'
    ENVIADO = 'Enviado', 'E'
    ENTREGADO = 'Entregado', 'Et'
    CANCELADO = 'Cancelado', 'C'

class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Asumiendo que Usuario está definido en tu modelo
    correo = models.EmailField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)
    estado = models.CharField(  # Cambia max_length a 1
        max_length=10,  # Cambiar aquí a 1 para que coincida con los valores de EstadoPedido
        choices=EstadoPedido.choices,
        default=EstadoPedido.PENDIENTE,
    )
    numero_compra = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    class Meta:
        permissions = [
            ("can_change_status", "Can change order status"),
        ]

class DetalleLibro(models.Model):
    libro = models.CharField(max_length=255) #titulo, no planeo cambiarlo 
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()
    pedido = models.ForeignKey(Pedido, related_name='detalle_libros', on_delete=models.CASCADE) # clave foranea al pedido