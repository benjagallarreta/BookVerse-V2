from decimal import Decimal
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from Carrito.models import Cart
from Pedidos.models import Pedido, DetalleLibro,Libro
from Usuario.models import Usuario 

@login_required #Esto de aca debe de cambiar a clase
def realizar_compra(request):
    #funcion crear pedido
    detalles_carrito = Cart.objects.filter(usuario=request.user)    
    usuario = request.user
    correo = usuario.email
    monto_total = total = sum(detalle.precio for detalle in detalles_carrito)
    # creo el pedido
    pedido = Pedido.objects.create( 
        usuario=usuario,
        correo=correo,
        monto_total=monto_total
    )
    #funcion crear detalle de los libros
    for item in detalles_carrito:
        DetalleLibro.objects.create(
            libro=item.libro.titulo,
            precio=item.precio,
            cantidad=item.cantidad,
            pedido=pedido
        )
    Cart.objects.filter(usuario=request.user).delete()

    return redirect ('compra_exitosa')

def detalle(request, numero_compra):
    # Obtén el pedido usando el número de compra
    pedido = get_object_or_404(Pedido, numero_compra=numero_compra)

    # Filtra los libros relacionados con ese pedido
    libros = DetalleLibro.objects.filter(pedido=pedido)

    usuario = pedido.usuario
    # Renderiza el template con el pedido y los libros
    return render(request, 'detalle.html', {'pedido': pedido, 'libros': libros, 'usuario': usuario})

