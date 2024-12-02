from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, View
from Carrito.models import Cart
from Pedidos.models import Libro
from Wishlist.models import WishList
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class WishListView(ListView):
    model = WishList
    template_name = 'wishlist.html'
    context_object_name = 'wishlist_items'

    def get_queryset(self):
        return WishList.objects.filter(usuario=self.request.user)

@method_decorator(login_required, name='dispatch')
class AgregarLibroWishList(View):
    def post(self, request, isbn):
        # No es necesario verificar nuevamente si el usuario está autenticado

        usuario = request.user
        libro = get_object_or_404(Libro, isbn=isbn)
        
        try:
            
            # Verifica si el libro ya está en la wish list del usuario
            wishlist_item, created = WishList.objects.get_or_create(usuario=usuario, libro=libro)
            
            if created:
                # Si no existía y se creó, el libro se agregó a la wishlist
                in_wishlist = True
            else:
                # Si ya existía, lo eliminamos de la wishlist
                wishlist_item.delete()
                in_wishlist = False

            return JsonResponse({'in_wishlist': in_wishlist})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
@method_decorator(login_required, name='dispatch')
class EliminarDeWishListView(View):
    def post(self, request, isbn):
        usuario = request.user
        libro = get_object_or_404(Libro, isbn=isbn)
        wishlist_item = get_object_or_404(WishList, usuario=usuario, libro=libro)
        wishlist_item.delete()
        return redirect('wishlist')

@method_decorator(login_required, name='dispatch')
class AgregarAlCarritoDesdeWishList(View):
    def post(self, request, isbn):
        usuario = request.user
        libro = get_object_or_404(Libro, isbn=isbn)
        # Agregar el libro al carrito
        carrito_item, created = Cart.objects.get_or_create(usuario=usuario, libro=libro, defaults={'precio': libro.precio})
        if not created:
            carrito_item.cantidad += 1
        carrito_item.precio = libro.precio * carrito_item.cantidad
        carrito_item.save()
        # Eliminar el libro de la wish list
        wishlist_item = get_object_or_404(WishList, usuario=usuario, libro=libro)
        wishlist_item.delete()
        return redirect('carrito')
