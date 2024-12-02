# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import PerfilUsuario

class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil de Usuario'
    fields = ('programa',)  # Solo mostrar el campo 'programa' en el admin

class UsuarioAdmin(UserAdmin):
    inlines = (PerfilUsuarioInline,)  # Mostrar el perfil de usuario en el admin

# Desregistramos el UserAdmin original y registramos el nuevo
admin.site.unregister(User)
admin.site.register(User, UsuarioAdmin)
