# admin.py
from django.contrib import admin
from .models import Libro

class LibroAdmin(admin.ModelAdmin):
    actions = ['vaciar_stock']  # Incluir vaciar_stock en la lista de acciones
    search_fields = ('isbn', 'titulo', 'autor', 'editorial', 'genero')
    list_display = ('titulo', 'autor', 'precio', 'genero', 'isbn', 'stock')  # Agregar 'stock' a list_display
    list_filter = ("genero","autor")
    # Acción para vaciar el stock
    def vaciar_stock(self, request, queryset):
        queryset.update(stock=0)  # Cambia el valor del stock a 0
        self.message_user(request, "El stock de los libros seleccionados ha sido actualizado a 0.")

    vaciar_stock.short_description = "Vaciar stock de los libros seleccionados"

admin.site.register(Libro, LibroAdmin)
