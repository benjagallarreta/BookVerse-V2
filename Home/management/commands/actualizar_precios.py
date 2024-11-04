import random
from django.core.management.base import BaseCommand
from Home.models import Libro  # Asegúrate de que la ruta sea correcta

class Command(BaseCommand):
    help = 'Asigna precios aleatorios a los libros'

    def handle(self, *args, **kwargs):
        libros = Libro.objects.all()
        for libro in libros:
            libro.precio = random.randint(12000, 40000)
            libro.save()
        self.stdout.write(self.style.SUCCESS('Precios actualizados exitosamente'))