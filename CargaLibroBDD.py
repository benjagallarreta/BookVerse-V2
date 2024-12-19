import os
import django
import requests
from django.utils.text import slugify

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookVerse.settings')
django.setup()

from Pedidos.models import Libro

# Lista de géneros a crear
nombres_generos = [
    "Romance", "Fantasy", "Science Fiction", "Mystery",
    "Horror", "Thriller", "Historical Fiction",
    "Woman's Fiction", "LGBTQ+", "Contemporary Fiction"
]

# Función para obtener libros de Google Books
def obtener_libros(query, max_results=40):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults={max_results}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        print(f"Error al obtener libros para la consulta '{query}': {response.status_code}")
        return []

import random

def cargar_libros(genero):
    libros = obtener_libros(genero)
    for libro in libros:
        info = libro['volumeInfo']
        titulo = info.get('title', 'Título desconocido')
        autores = ", ".join(info.get('authors', ['Autor desconocido']))
        isbn_list = [identifier['identifier'] for identifier in info.get('industryIdentifiers', []) if identifier['type'] == 'ISBN_13']
        isbn = isbn_list[0] if isbn_list else None
        if isbn is None:
            continue  # Salta libros sin ISBN
        sinopsis = info.get('description', f"Libro sobre {genero}")
        portada = info.get('imageLinks', {}).get('thumbnail', None)
        editorial = info.get('publisher', 'Editorial desconocida')
        precio = random.randint(12000, 40000)
        # Genera un valor de stock aleatorio entre 0 y 100
        stock = random.randint(0, 100)

        Libro.objects.create(
            titulo=titulo,
            autor=autores,
            sinopsis=sinopsis,
            isbn=isbn,
            genero=genero,
            editorial=editorial,
            portada=portada,
            stock=stock,
            precio=precio
        )

        print(f"Libro '{titulo}' creado con stock {stock}.")


# Cargar al menos 1000 libros distribuidos en los 10 géneros
libros_por_genero = 100
for genero in nombres_generos:
    cargar_libros(genero)

print("Carga de libros completada.")