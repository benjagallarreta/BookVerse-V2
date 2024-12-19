import os
import django
from decimal import Decimal
import random

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookVerse.settings')
django.setup()

# Importar el modelo de Libro
from Pedidos.models import Libro

# Función para actualizar el stock y el precio de todos los libros
def actualizar_stock_precio():
    libros = Libro.objects.all()  # Obtener todos los libros
    for libro in libros:
        # Establecer un nuevo precio aleatorio (por ejemplo, entre 10.00 y 500.00)
        nuevo_precio = round(random.uniform(10000.00, 50000.00), 2)
        # Establecer un nuevo stock aleatorio (por ejemplo, entre 0 y 100)
        nuevo_stock = random.randint(0, 100)

        # Actualizar los campos de precio y stock
        libro.precio = Decimal(nuevo_precio)
        libro.stock = nuevo_stock

        # Guardar los cambios en la base de datos
        libro.save()

        print(f"Libro '{libro.titulo}' actualizado - Precio: {nuevo_precio}, Stock: {nuevo_stock}")

# Ejecutar la función
actualizar_stock_precio()

print("Actualización de precios y stock completada.")
