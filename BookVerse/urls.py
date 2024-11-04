from django import views
from django.contrib import admin
from django.urls import path
from Home.views import HomeView, LibrosPorGeneroView
from Usuario.views import LoginView, CustomLogoutView, RegistroView, UsuarioDetailView, UsuarioUpdateView, RedirectToAdminView
from Pedidos.views import realizar_compra, detalle
from Carrito.views import CarritoView,AgregarLibroView, CheckOutView, CompraExitosaView, errorCompra,EliminarLibroView,RestarLibroView,LimpiarCarritoView,PaymentView
from Wishlist.views import AgregarAlCarritoDesdeWishList, EliminarDeWishListView, WishListView,AgregarLibroWishList
from Reseña.views import AgregarResenaView, DetailLibroView
urlpatterns = [
    #home y libro
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),   
    path('libros/<str:genero>/', LibrosPorGeneroView.as_view(), name='libros_por_genero'),
    #path('libro/<str:isbn>/', LibroDetailView.as_view(), name='libro_detallado'),

    #usuario
    path('perfil/', UsuarioDetailView.as_view(), name='perfil_usuario'),
    path('editar-perfil/', UsuarioUpdateView.as_view(), name='editar_usuario'),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('acceso-admin/',RedirectToAdminView.as_view(), name='acceso_admin'),

    #pedidos
    path('generar_pedido/',realizar_compra,name='generar_pedido'),
    path('detalle/<uuid:numero_compra>/', detalle, name='detalle'),

    #carrito 
    path('compra-exitosa/', CompraExitosaView.as_view(), name='compra_exitosa'),
    path('compra-rechazada/', errorCompra.as_view(), name='compra_rechazada'),
    path('carrito/', CarritoView.as_view(), name='carrito'),
    path('agregar/<str:isbn>/', AgregarLibroView.as_view(), name='agregar_libro'),
    path('eliminar/<str:isbn>/', EliminarLibroView.as_view(), name='eliminar_libro'),
    path('restar/<str:isbn>/', RestarLibroView.as_view(), name='restar_libro'),
    path('limpiar/', LimpiarCarritoView.as_view(), name='limpiar_carrito'),
    path('checkout/', CheckOutView.as_view(), name='checkout'),
    path('pago/', PaymentView.as_view(), name='pago'),

    #wishlist
    path('wishlist/', WishListView.as_view(), name='wishlist'),
    path('agregar_a_wishlist/<str:isbn>/', AgregarLibroWishList.as_view(), name='agregar_a_wishlist'),
    path('eliminar_de_wishlist/<str:isbn>/', EliminarDeWishListView.as_view(), name='eliminar_de_wishlist'),
    path('agregar_al_carrito_desde_wishlist/<str:isbn>/', AgregarAlCarritoDesdeWishList.as_view(), name='agregar_al_carrito_desde_wishlist'),


    #reseña
    path('libro/<str:isbn>/agregar-resena/', AgregarResenaView.as_view(), name='agregar_resena'),
    path('libro/<str:isbn>/libroDetalle', DetailLibroView.as_view(), name='detalle_libro'),

    
]
 