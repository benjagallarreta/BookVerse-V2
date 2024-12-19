from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from Reseña.forms import ReseñaForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from Home.models import Libro
from Reseña.models import Reseña  
from django.db.models import Avg
from Reseña.forms import ReseñaForm
from Wishlist.models import WishList

class DetailLibroView(View):
    def get(self, request,isbn):
        # Obtener el libro por el ISBN
        libro = get_object_or_404(Libro, isbn=isbn)

        # Filtrar las reseñas del libro
        resenas = Reseña.objects.filter(libro=libro)

        # Calcular el total de reseñas
        total_resenas = resenas.count()

        # Calcular el promedio de estrellas de las reseñas
        if total_resenas > 0:
            promedio_estrellas = round(resenas.aggregate(promedio=Avg('estrellas'))['promedio'], 2)
        else:
            promedio_estrellas = 0  # Si no hay reseñas, el promedio es 0

        # Crear el contexto para la plantilla
        context = {
            'libro': libro,
            'resenas': resenas,
            'total_resenas': total_resenas,
            'promedio_estrellas': promedio_estrellas,  # Añadir el promedio al contexto
            'form': ReseñaForm(),
        }

        # Agregar información de wishlist si el usuario está autenticado
        if request.user.is_authenticated:
            wishlist_items = WishList.objects.filter(
                usuario=request.user
            ).values_list('libro__isbn', flat=True)
            context['wishlist_items'] = list(wishlist_items)
            
        # Retornar el resultado a la plantilla Item.html
        return render(request, 'Item.html', context)

            
@method_decorator(login_required, name='dispatch')
class AgregarResenaView(View):
    def post(self, request, isbn):
        libro = get_object_or_404(Libro, isbn=isbn)
        form = ReseñaForm(request.POST)
        
        if form.is_valid():
            reseña = form.save(commit=False)
            reseña.usuario = request.user
            reseña.libro = libro
            reseña.save()
        
        # Si el formulario no es válido, redirige de nuevo a la vista de detalle del libro
        return redirect(reverse('detalle_libro', kwargs={'isbn': isbn}))
