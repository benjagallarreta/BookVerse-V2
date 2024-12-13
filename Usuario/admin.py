from django.contrib import admin
from .models import Usuario

class UsuarioAdmin(admin.ModelAdmin):
    search_fields = ('nombre_completo','username','provincia','nacionalidad','email','is_active')
    list_display = ('nombre_completo','username','provincia','nacionalidad','email','is_active')
    actions = ['eliminacion_Logica_usuarios','activacion_Logica_usuarios']
    list_filter = ("is_active","is_staff")
    def eliminacion_Logica_usuarios(self,reuquest,queryset):
        for usuario in queryset:
            usuario.is_active=False
            usuario.save()

    def activacion_Logica_usuarios(self,reuquest,queryset):
        for usuario in queryset:
            usuario.is_active=True
            usuario.save()
            
# Register your models here.
admin.site.register(Usuario, UsuarioAdmin)