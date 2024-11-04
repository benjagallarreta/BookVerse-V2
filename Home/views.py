from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView, DetailView
from django.db.models import Q
from Home.models import Libro
from Reseña.forms import ReseñaForm
from Reseña.models import  Reseña



class HomeView(ListView):
    model = Libro
    template_name = 'home.html'
    context_object_name = 'libros'
    paginate_by = 20

    # Resultado de busqueda 
    def get_queryset(self):
        queryset = Libro.objects.all()
        search_query = self.request.GET.get('buscar')

        if search_query:
            queryset = queryset.filter(
                Q(titulo__icontains=search_query) |
                Q(autor__icontains=search_query) |
                Q(isbn__icontains=search_query)
            )

        return queryset
    
class LibrosPorGeneroView(View):
    def get(self, request, genero):
        libros = Libro.objects.filter(genero__icontains=genero)
        context = {
            'libros': libros,
            'genero': genero
        }
        return render(request, 'libros_por_genero.html', context)

