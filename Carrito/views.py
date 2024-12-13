
from decimal import Decimal
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

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

        # Si se pasa de los 100,000 no puede realizar la compra, sino si puede
        if total > Decimal('100000'):
            return redirect('compra_rechazada')
        else:
            context = {
                'total': total,
            }
            return redirect('pago')
        

@method_decorator(login_required, name='dispatch')
class PaymentView(View):
    template_name = 'payment.html'

    def get_total(self, user):
        return Cart.objects.filter(usuario=user).aggregate(total=Sum('precio'))['total'] or Decimal('0.00')

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
            # Procesar el pago aquí
            return redirect('generar_pedido')
        context = {
            'form': form,
            'total': total
        }
        return render(request, 'payment.html', {'form': form})
