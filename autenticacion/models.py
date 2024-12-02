from django.db import models
from django.contrib.auth.models import User
from actividades.models import Programa
import os
from django.utils.text import slugify

def generar_ruta_foto_perfil(instance, filename):
    """Genera la ruta personalizada para la foto de perfil del usuario."""
    nombre_usuario = slugify(instance.user.username)  # Usa el nombre de usuario para generar la ruta
    extension = filename.split('.')[-1]  # Obtiene la extensión del archivo original
    nuevo_nombre_archivo = f'{nombre_usuario}.{extension}'  # Nuevo nombre del archivo
    return os.path.join('perfil_usuarios/', nuevo_nombre_archivo)  # Devuelve la nueva ruta para la foto de perfil

def generar_ruta_foto_firma(instance, filename):
    """Genera la ruta personalizada para la firma del usuario."""
    nombre_usuario = slugify(instance.user.username)  # Usa el nombre de usuario para generar la ruta
    extension = filename.split('.')[-1]  # Obtiene la extensión del archivo original
    nuevo_nombre_archivo = f'{nombre_usuario}_firma.{extension}'  # Nuevo nombre del archivo de firma
    return os.path.join('firmas_usuarios/', nuevo_nombre_archivo)

class PerfilUsuario(models.Model):
    img_firma = models.ImageField(upload_to=generar_ruta_foto_firma,default='default/sin_firmar.png')
    img_usuario = models.ImageField(upload_to=generar_ruta_foto_perfil, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    programa = models.ForeignKey(Programa, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.programa}"

    def save(self, *args, **kwargs):
        try:
            this = PerfilUsuario.objects.get(id=self.id)
            # Si se sube una nueva firma y la firma actual NO es la misma
            if self.img_firma and self.img_firma != this.img_firma:
                # Si existe una firma anterior, la eliminamos
                if this.img_firma.name != 'default/sin_firmar.png' and os.path.isfile(this.img_firma.path):
                        os.remove(this.img_firma.path)        
            # Si se sube una nueva imagen de usuario y la imagen actual NO es la misma
            if self.img_usuario and self.img_usuario != this.img_usuario:
                # Si existe una imagen anterior, la eliminamos
                if this.img_usuario and os.path.isfile(this.img_usuario.path):
                    os.remove(this.img_usuario.path)
        except PerfilUsuario.DoesNotExist:
            # El perfil no existe todavía en la base de datos (es nuevo)
            pass
        # Guardar la nueva instancia de PerfilUsuario
        super().save(*args, **kwargs)


    
