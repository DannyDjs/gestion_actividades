# sga/urls.py
from django.urls import include, path
from django.conf.urls.static import static
from SGA import settings
from . import views
from .views import DescargarReporte

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('obtener_arbol_tipo_actividad/<int:tipo_id>/', views.obtener_arbol_tipo_actividad, name='obtener_arbol_tipo_actividad'),
    path('perfil/', views.perfil, name='perfil'),
    
    path('agregar_actividad/', views.agregar_actividad, name='agregar_actividad'),
    path('listar_actividad/', views.listar_actividad, name='listar_actividad'),
    path('editar_actividad/', views.editar_actividad, name='editar_actividad'),
    path('eliminar_actividad/<int:actividad_id>/', views.eliminar_actividad, name='eliminar_actividad'),
    
    path('informes/<int:actividad_id>/', views.listar_informe, name='listar_informe'),
    path('actividad/<int:actividad_id>/firmar_todos_informes/', views.firmar_todos_informes, name='firmar_todos_informes'),
    path('informe/agregar/<int:actividad_id>', views.agregar_informe, name='agregar_informe'),
    path('informe/editar/<int:informe_id>/', views.editar_informe, name='editar_informe'),
    path('editar-informe-modal/<int:informe_id>/', views.editar_informe_modal, name='editar_informe_modal'),
    path('eliminar_informe/<int:informe_id>/', views.eliminar_informe, name='eliminar_informe'),
    path('informe/firmar/<int:informe_id>/', views.firmar_informe, name='firmar_informe'),
    
    path('eliminar_evidencia/<int:evidencia_id>/', views.eliminar_evidencia, name='eliminar_evidencia'),
    
    path('tipos/', views.listar_tipos, name='listar_tipos'),
    path('tipos/agregar/', views.agregar_tipo, name='agregar_tipo'),
    path('tipos/editar/', views.editar_tipo, name='editar_tipo'),
    path('tipos/eliminar/<int:tipo_id>/', views.eliminar_tipo, name='eliminar_tipo'),
    
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/agregar/', views.agregar_usuario, name='agregar_usuario'),
    path('usuarios/agregar/csv', views.cargar_usuarios_csv, name='cargar_usuarios_csv'),
    path('usuarios/editar/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    
    path('actividad/<int:actividad_id>/descargar/<str:formato>/', DescargarReporte.as_view(), name='descargar_reporte'),
    path('descargar-informe/',views.generar_informe_pdf, name='generar_informe_pdf'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)