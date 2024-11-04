from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import DetalleLibro, Pedido, EstadoPedido
from .forms import CambiarEstadoForm
from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import CambiarEstadoForm
from .models import Pedido

class PedidoAdmin(admin.ModelAdmin):
    actions = ['cambiar_estado_a_pendiente','cambiar_estado_a_enviado','cambiar_estado_a_entregado','cambiar_estado_a_cancelado']
    search_fields = ('usuario__username', 'numero_compra', 'correo', 'estado')
    list_display = ('usuario', 'numero_compra', 'correo','fecha','estado')

    def cambiar_estado_a_pendiente(modeladmin, request, queryset):
        queryset.update(estado=EstadoPedido.PENDIENTE)
    cambiar_estado_a_pendiente.short_description = "Cambiar estado a Pendiente"

    def cambiar_estado_a_enviado(modeladmin, request, queryset):
        queryset.update(estado=EstadoPedido.ENVIADO)
    cambiar_estado_a_enviado.short_description = "Cambiar estado a Enviado"

    def cambiar_estado_a_entregado(modeladmin, request, queryset):
        queryset.update(estado=EstadoPedido.ENTREGADO)
    cambiar_estado_a_entregado.short_description = "Cambiar estado a Entregado"

    def cambiar_estado_a_cancelado(modeladmin, request, queryset):
        queryset.update(estado=EstadoPedido.CANCELADO)
    cambiar_estado_a_cancelado.short_description = "Cambiar estado a Cancelado"

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']  # Eliminar la acción de "Eliminar seleccionados"
        return actions
    
admin.site.register(Pedido, PedidoAdmin)