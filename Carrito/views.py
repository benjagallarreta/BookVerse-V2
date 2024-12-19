
from decimal import ROUND_DOWN, Decimal
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db import transaction
from Carrito.forms import PaymentForm
from Home.models import Libro 
from Carrito.models import Cart 

@method_decorator(login_required, name='dispatch')
class CarritoView(ListView):
    model = Libro
    template_name = 'Carrito.html'  
    context_object_name = 'libros'

    def get_queryset(self):
        # Obtiene los libros que están en el carrito del usuario
        # Si el carrito está vacío, el QuerySet también lo estará
        return Libro.objects.filter(cart__usuario=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtiene el carrito del usuario
        context['carrito'] = Cart.objects.filter(usuario=self.request.user)
        # Calcula el total del carrito
        cart_items = context['carrito']
        total = sum(item.precio for item in cart_items)
        # Agrega el total al contexto
        context['total'] = total
        return context

@method_decorator(login_required, name='dispatch')
class AgregarLibroView(View):
    def post(self, request, isbn):
        usuario = request.user
        libro = get_object_or_404(Libro, isbn=isbn)
        carrito_item, created = Cart.objects.get_or_create(usuario=usuario, libro=libro, defaults={'precio': libro.precio})
        if not created:
            carrito_item.cantidad += 1
        carrito_item.precio = libro.precio * carrito_item.cantidad 
        carrito_item.save()
        referer = request.META.get('HTTP_REFERER', 'home')
        return HttpResponseRedirect(referer)

    def get(self, request,isbn):
        return self.post(request,isbn)

    
class EliminarLibroView(View):
    def post(self, request, isbn):
        usuario = request.user
        libro = get_object_or_404(Libro, isbn=isbn)
        carrito_item = get_object_or_404(Cart, usuario=usuario, libro=libro)
        carrito_item.delete()

        return redirect('carrito')

class RestarLibroView(View):
    def post(self, request, isbn):
        usuario = request.user
        libro = get_object_or_404(Libro, isbn=isbn)
        carrito_item = get_object_or_404(Cart, usuario=usuario, libro=libro)
        if carrito_item.cantidad > 1:
            carrito_item.cantidad -= 1
            carrito_item.precio = libro.precio * carrito_item.cantidad
            carrito_item.save()
        else:
            carrito_item.delete()
        
        return redirect('carrito')

class LimpiarCarritoView(View):
    def post(self, request):
        usuario = request.user
        Cart.objects.filter(usuario=usuario).delete()

        return redirect('carrito')

@method_decorator(login_required, name='dispatch')
class CompraExitosaView(View):
    template_name = 'CompraRealizada.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

@method_decorator(login_required, name='dispatch')  
class errorCompra(View):
    template_name = 'errorCompra.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

@method_decorator(login_required, name='dispatch')
class CheckOutView(View):
    def get(self, request, *args, **kwargs):
        total = Cart.objects.filter(usuario=request.user).aggregate(total=Sum('precio'))['total'] or 0

        if total == Decimal('0.00'):
            return redirect('/')
        context = {
            'total': total,
        }
        # Obtener los elementos del carrito
        carrito_items = Cart.objects.filter(usuario=request.user)

        # Verificar si hay suficiente stock para cada libro en el carrito
        for item in carrito_items:
            libro = item.libro
            if libro.stock < item.cantidad:
                # Si algún libro no tiene suficiente stock, redirigir a una página de error
                return redirect('compra_rechazada')  # Cambiar a una vista con un mensaje específico si lo prefieres

        # Si todo está bien, procesar la compra y decrementar el stock
        with transaction.atomic():
            for item in carrito_items:
                libro = item.libro
                libro.stock -= item.cantidad  # Decrementar el stock
                libro.save()  # Guardar los cambios en la base de datos
        
        # Redirigir al proceso de pago
        return redirect('pago')        

@method_decorator(login_required, name='dispatch')
class PaymentView(View):
    template_name = 'payment.html'

    def get_total(self, user):
        return Cart.objects.filter(usuario=user).aggregate(total=Sum('precio'))['total'] or Decimal('0.00')
    
    def get_total(self, user):
        total = Cart.objects.filter(usuario=user).aggregate(total=Sum('precio'))['total'] or Decimal('0.00')
        # Redondear a 2 decimales
        return total.quantize(Decimal('0.01'), rounding=ROUND_DOWN)

    def get(self, request):
        form = PaymentForm()
        total = self.get_total(request.user)
        context = {
            'form': form,
            'total': total
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = PaymentForm(request.POST)
        total = self.get_total(request.user)
        
        if form.is_valid():
            # Aquí puedes agregar la lógica de procesamiento del pago
            try:
                # Procesar el pago
                return redirect('generar_pedido')
            except Exception as e:
                form.add_error(None, "Error procesando el pago: {}".format(str(e)))
        
        # Si hay errores, mostrar el formulario con los errores
        context = {
            'form': form,
            'total': total,
        }
        return render(request, self.template_name, context)