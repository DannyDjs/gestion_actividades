# signals.py
from django.db.models.signals import post_save,pre_save,post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from autenticacion.models import PerfilUsuario
from .models import Actividad, Informe, AuditoriaActividad, AuditoriaInforme
from django.utils import timezone
import json

@receiver(post_save, sender=User)
def manejar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        # Verificar si ya existe un perfil para el usuario
        if not hasattr(instance, 'perfilusuario'):
            perfil_usuario = PerfilUsuario.objects.create(user=instance)
            
            # Si el creador tiene perfil, asignar la facultad y el programa
            if hasattr(instance, 'creator') and instance.creator.perfilusuario:
                creator_profile = instance.creator.perfilusuario
                perfil_usuario.programa = creator_profile.programa
                perfil_usuario.save()

    else:
        # Si el usuario ya existe, guardar el perfil si es necesario
        if hasattr(instance, 'perfilusuario'):
            instance.perfilusuario.save()
            
        
@receiver(pre_save, sender=Actividad)
def guardar_valor_anterior(sender, instance, **kwargs):
    if instance.pk:  # Si el objeto ya existe
        # Actualiza el objeto actual desde la base de datos para obtener los valores previos
        original = Actividad.objects.filter(pk=instance.pk).only('descripcion').first()
        if original and original.descripcion != instance.descripcion:
            instance._original_descripcion = original.descripcion

@receiver(post_save, sender=Actividad)
def crear_auditoria_actividad(sender, instance, created, **kwargs):
    if created:
        AuditoriaActividad.objects.create(
            actividad=instance,
            estado_anterior='',
            estado_actual=instance.descripcion or 'Sin descripción',
            accion="Creación",
            modificado_por=instance.creado_por,
            fecha_modificacion=timezone.now()
        )
    else:
        estado_anterior = getattr(instance, '_original_descripcion', instance.descripcion)
        estado_actual = instance.descripcion or 'Sin descripción'
        
        if estado_anterior != estado_actual:
            AuditoriaActividad.objects.create(
                actividad=instance,
                estado_anterior=estado_anterior,
                estado_actual=estado_actual,
                accion="Actualización",
                modificado_por=instance.creado_por,
                fecha_modificacion=timezone.now()
            )
# Auditoría para eliminaciones de informe
@receiver(post_delete, sender=Actividad)
def crear_auditoria_actividad_eliminado(sender, instance, **kwargs):
    # Crear un registro de auditoría cuando la actividad sea eliminada
    # Primero aseguramos que los informes asociados existan
    informes_asociados = Informe.objects.filter(actividad=instance)
    
    for informe in informes_asociados:
        AuditoriaInforme.objects.create(
            informe=informe,
            estado_anterior=informe.contenido or 'sin contenido',
            estado_actual='Eliminado',
            modificado_por=instance.creado_por,  # El usuario que eliminó la actividad
            fecha_modificacion=timezone.now(),
            accion="Eliminación"
        )

# Capturar cambios en los informes antes de guardarlos
@receiver(pre_save, sender=Informe)
def guardar_valor_anterior(sender, instance, **kwargs):
    if instance.pk:  # Si el objeto ya existe
        # Actualiza el objeto original desde la base de datos para obtener los valores previos
        original = Informe.objects.filter(pk=instance.pk).only('contenido').first()
        if original and original.contenido != instance.contenido:
            instance._original_contenido = original.contenido

# Crear auditoría de informe después de que se guarde
@receiver(post_save, sender=Informe)
def crear_auditoria_informe(sender, instance, created, **kwargs):
    if created:  # Si el informe es nuevo
        estado_anterior = ''  # Estado inicial
        estado_actual = instance.contenido or 'Sin contenido',
        AuditoriaInforme.objects.create(
            informe=instance,
            estado_anterior=estado_anterior,
            estado_actual=estado_actual,
            modificado_por=instance.usuario,  # El usuario que creó el informe
            fecha_modificacion=timezone.now(),
            accion="Creación"
        )
    else:  # Si el informe fue actualizado
        estado_anterior = getattr(instance, '_original_contenido', instance.contenido)
        estado_actual = instance.contenido or 'sin contenido'
        
        if estado_anterior != estado_actual:
            AuditoriaInforme.objects.create(
                informe=instance,
                estado_anterior=estado_anterior,
                estado_actual=estado_actual,
                modificado_por=instance.usuario,  # El usuario que modificó el informe
                fecha_modificacion=timezone.now(),
                accion="Actualización"
            )

@receiver(post_delete, sender=Informe)
def crear_auditoria_informe_eliminado(sender, instance, **kwargs):
    # Verificar si el informe todavía existe antes de intentar crear la auditoría
    try:
        # Verifica si la instancia aún existe en la base de datos
        informe = Informe.objects.get(pk=instance.pk)
    except Informe.DoesNotExist:
        return

    # Crear un registro de auditoría cuando el informe sea eliminado
    AuditoriaInforme.objects.create(
        informe=informe,
        estado_anterior=informe.contenido or 'Desconocido',
        estado_actual='Eliminado',
        modificado_por=informe.usuario,  # El usuario que eliminó el informe
        fecha_modificacion=timezone.now(),
        accion="Eliminación"
    )