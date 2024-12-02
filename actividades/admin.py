from django.contrib import admin
from .models import TipoActividad,Actividad,Facultad,Programa,AuditoriaActividad, AuditoriaInforme

# Register your models here.
admin.site.register(TipoActividad)
admin.site.register(Actividad)
admin.site.register(Facultad)
admin.site.register(Programa)

# Configuración de la administración de AuditoriaActividad
class AuditoriaActividadAdmin(admin.ModelAdmin):
    list_display = ('actividad', 'estado_anterior', 'estado_actual', 'modificado_por','accion', 'fecha_modificacion')
    list_filter = ('estado_actual', 'modificado_por')  # Agregar filtros para facilitar la búsqueda
    search_fields = ('actividad__titulo', 'estado_anterior', 'estado_actual')  # Permite buscar por nombre de la actividad

# Configuración de la administración de AuditoriaInforme
class AuditoriaInformeAdmin(admin.ModelAdmin):
    list_display = ('informe', 'estado_anterior', 'estado_actual', 'modificado_por', 'fecha_modificacion')
    list_filter = ('estado_actual', 'modificado_por')  # Agregar filtros para facilitar la búsqueda
    search_fields = ('informe__titulo', 'estado_anterior', 'estado_actual')  # Permite buscar por nombre del informe
    
admin.site.register(AuditoriaActividad, AuditoriaActividadAdmin)
admin.site.register(AuditoriaInforme, AuditoriaInformeAdmin)