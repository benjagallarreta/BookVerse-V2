from django import forms
from .models import EstadoPedido

class CambiarEstadoForm(forms.Form):
    estado = forms.ChoiceField(choices=EstadoPedido.choices, label="Nuevo Estado")
