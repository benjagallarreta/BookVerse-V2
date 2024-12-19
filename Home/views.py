from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.db.models import Q
from Home.models import Libro
from Wishlist.models import WishList  # Añade esta importación

class HomeView(ListView):
    model = Libro
    template_name = 'home.html'
    context_object_name = 'libros'
    paginate_by = 20
    ordering = ['titulo']

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            wishlist_items = WishList.objects.filter(
                usuario=self.request.user
            ).values_list('libro__isbn', flat=True)
            context['wishlist_items'] = list(wishlist_items)
        return context
    
class LibrosPorGeneroView(View):
    def get(self, request, genero):
        libros = Libro.objects.filter(genero__icontains=genero)
        context = {
            'libros': libros,
            'genero': genero
        }

        # Añadir información de wishlist si el usuario está autenticado
        if request.user.is_authenticated:
            wishlist_items = WishList.objects.filter(
                usuario=request.user
            ).values_list('libro__isbn', flat=True)
            context['wishlist_items'] = list(wishlist_items)

        return render(request, 'libros_por_genero.html', context)