from django import forms
from .models import Reseña

class ReseñaForm(forms.ModelForm):
    class Meta:
        model = Reseña
        fields = ['comentario', 'estrellas']
        widgets = {
            'comentario': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Escribe tu reseña...',
                'style': 'min-height: 30px; max-height: 60px; padding: 1rem; border-radius: 10px; overflow-y: auto; resize: none;',
            }),
            'estrellas': forms.RadioSelect(choices=[(i, f'{i} estrella(s)') for i in range(1, 6)]),
        }
