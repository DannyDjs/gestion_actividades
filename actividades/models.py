from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.text import slugify
import os

# Modelo para Facultad
class Facultad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


# Modelo para Programa
class Programa(models.Model):
    nombre = models.CharField(max_length=100)
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, related_name='programas')

    class Meta:
        unique_together = ('nombre', 'facultad')

    def __str__(self):
        return f"{self.nombre} - {self.facultad.nombre}"

# Modelo para Tipo de Actividades
class TipoActividad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    #programa = models.ForeignKey(Programa, on_delete=models.SET_NULL, null=True, blank=True)
    programa = models.ForeignKey(Programa, on_delete=models.SET_NULL, null=True, related_name="tipos_actividades")


    def __str__(self):
        return self.nombre

def generar_ruta_foto_actividad(instance, filename):
    """Genera la ruta personalizada para la foto de la actividad."""
    nombre_actividad = slugify(instance.titulo)  # Combina el nombre de la actividad
    extension = filename.split('.')[-1]  # Obtiene la extensión del archivo original
    nuevo_nombre_archivo = f'{nombre_actividad}.{extension}'  # Nuevo nombre del archivo
    return os.path.join('actividades/', nuevo_nombre_archivo)

# Modelo para Actividades
class Actividad(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    lugar = models.CharField(max_length=100,default='')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    imagen = models.ImageField(upload_to=generar_ruta_foto_actividad, null=True, blank=True)  # Campo para imagen de la actividad
    tipo = models.ForeignKey(TipoActividad, on_delete=models.SET_NULL, null=True)
    colaborador = models.ManyToManyField(User, related_name='actividades_asignadas')
    
    estado = models.CharField(max_length=20, default='Pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='actividades_creadas')

    def verificar_informes(self):
        """Verifica el estado de la actividad según los informes."""
        total_usuarios = self.colaborador.count()
        informes = self.informes.all()  # Asegúrate de que 'informes' sea el nombre correcto
        
        # Verificar si hay informes
        if not informes.exists():
            self.estado = 'Pendiente'
            self.save()
            return
        
        # Verificar si hay informes sin firmar
        if any(InformeFirmado.objects.filter(informe=informe, estado_firma=True).count() < total_usuarios for informe in informes):
            self.estado = 'En Proceso'
        else:
            self.estado = 'Finalizada'
        
        self.save()

    def clean(self):
        if self.fecha_fin < self.fecha_inicio:
            raise ValidationError('La fecha de fin debe ser posterior a la fecha de inicio.')

    def __str__(self):
        return self.titulo



# Modelo para Informes
class Informe(models.Model):
    titulo = models.CharField(max_length=100,  default='')
    contenido = models.TextField()
    fecha_inicio = models.DateField(default='')  # Campo de fecha de inicio
    fecha_fin = models.DateField(default='')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name='informes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        # Cuando se crea o guarda un informe, el estado de la actividad pasa a 'Pendiente'
        if not self.pk:  # Solo se ejecuta si es un informe nuevo
            self.actividad.estado = 'Pendiente'
            self.actividad.save()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Informe de {self.actividad.titulo}"
    
    
class InformeFirmado(models.Model):
    informe = models.ForeignKey(Informe, related_name='firmas', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_firma = models.DateTimeField(auto_now_add=True)
    estado_firma = models.BooleanField(default=False)  # False = No Firmado, True = Firmado
    

    class Meta:
        unique_together = ('informe', 'usuario')  # Asegura que un usuario solo firme una vez un informe

    def __str__(self):
        estado = 'Firmado' if self.estado_firma else 'No Firmado'
        return f'Firma de {self.usuario.username} para {self.informe} - {estado}'
    
    
class AuditoriaActividad(models.Model):
    actividad = models.ForeignKey(Actividad, on_delete=models.SET_NULL, null=True)
    estado_anterior = models.TextField(null=True)
    estado_actual = models.TextField(null=True)
    accion = models.TextField(null=True)
    modificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Modificación de {self.actividad.titulo} por {self.modificado_por.username}"

class AuditoriaInforme(models.Model):
    informe = models.ForeignKey(Informe, on_delete=models.SET_NULL, null=True)
    estado_anterior = models.TextField(null=True)
    estado_actual = models.TextField(null=True)
    accion = models.TextField(null=True)
    modificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Modificación de informe {self.informe.actividad.titulo} por {self.modificado_por.username}"


class Evidencia(models.Model):
    informe = models.ForeignKey(Informe, related_name='evidencias', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='evidencias/', blank=True, null=True)
    archivo = models.FileField(upload_to='evidencias/', blank=True, null=True)
    enlace = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Evidencia para {self.informe.actividad.titulo}"
    
