from audioop import avg
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from Reseña.forms import ReseñaForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from Home.models import Libro
from Reseña.models import Reseña  
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, render
from django.views import View
from Home.models import Libro
from Reseña.models import Reseña
from Reseña.forms import ReseñaForm

from django.views import View
from django.shortcuts import get_object_or_404, render
from django.db.models import Avg
from .models import Libro, Reseña
from .forms import ReseñaForm

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
            promedio_estrellas = resenas.aggregate(promedio=Avg('estrellas'))['promedio']
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

""""
def contar_resenas_positivas(request,isbn):
    # Para pruebas, fijamos el ISBN directamente
      # ISBN de prueba

    # Obtener el libro por el ISBN fijo
    libro = get_object_or_404(Libro, isbn=isbn)

    # Filtrar las reseñas del libro con estrellas entre 3 y 5
    resenas_positivas = Reseña.objects.filter(libro=libro)

    # Calcular el promedio de estrellas de las reseñas positivas
    total_resenas_positivas = resenas_positivas.count()

    if total_resenas_positivas > 0:
        promedio_estrellas = resenas_positivas.aggregate(promedio=Avg('estrellas'))['promedio']
    else:
        promedio_estrellas = 0  # Si no hay reseñas, el promedio es 0

    # Retornar el resultado en formato JSON o como prefieras
    return render(request, 'prueba.html', {'promedio_estrellas': promedio_estrellas})
"""