from datetime import date
from django import forms
from django.contrib.auth.models import User,Group
from actividades.models import Actividad, Informe, TipoActividad,Evidencia
from autenticacion.models import PerfilUsuario


# Formulario para TipoActividad
class TipoActividadForm(forms.ModelForm):
    class Meta:
        model = TipoActividad
        fields = ['nombre']
        labels = {
            'nombre': 'Nombre del Tipo de Actividad',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            
        }

# Formulario para Actividad
class ActividadForm(forms.ModelForm):
    # Obtener los grupos deseados ('Profesor' y 'Director')
    profesores_group = Group.objects.get(name='Profesor')
    directores_group = Group.objects.get(name='Director')
    
    # Obtener los usuarios que pertenecen a cualquiera de los dos grupos
    colaborador = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__in=[profesores_group, directores_group]).distinct(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'colaborador-select','name': 'colaborador'}),
        required=True
    )
    
    class Meta:
        model = Actividad
        fields = ['titulo', 'descripcion', 'lugar','fecha_inicio','fecha_fin','imagen','tipo', 'colaborador']
        labels = {
            'titulo': 'Título de la Actividad',
            'descripcion': 'Descripción',
            'fecha_inicio': 'Fecha inicio de la Actividad',
            'fecha_fin': 'Fecha fin de la Actividad',
            'lugar': 'Lugar',
            'imagen': 'Imagen',
            'tipo': 'Tipo de Actividad',
            'colaborador': 'Colaboradores',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'lugar': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control-file'}),
            'tipo': forms.Select(attrs={'class': 'form-control', 'name': 'tipo'}),
            
        }

    def __init__(self, *args, **kwargs):
        # Obtener el programa del usuario autenticado
        programa_usuario = kwargs.pop('programa_usuario', None)
        super().__init__(*args, **kwargs)
        self.fields['colaborador'].widget.attrs.update({'multiple': 'multiple'})
        self.fields['imagen'].widget.attrs['accept'] = 'image/*'
        # Sobrescribir el método para mostrar el nombre y apellido en lugar del nombre de usuario
        self.fields['colaborador'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"
        if programa_usuario:
            self.fields['tipo'].queryset = TipoActividad.objects.filter(programa=programa_usuario)
            # Filtrar los colaboradores según el programa del usuario
            self.fields['colaborador'].queryset = User.objects.filter(
                perfilusuario__programa=programa_usuario
            )
          
# Formulario para Informe
class InformeForm(forms.ModelForm):
    class Meta:
        model = Informe
        fields = ['titulo','fecha_inicio','fecha_fin']
        labels = {
            'titulo': 'Título :',
            'fecha_inicio': 'Fecha inicio del Informe',
            'fecha_fin': 'Fecha fin del Informe',
            
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date','id':'id_fecha_inicio','class': 'form-control'}, format='%Y-%m-%d'),
            'fecha_fin': forms.DateInput(attrs={'type': 'date','id':'id_fecha_fin','class': 'form-control'}, format='%Y-%m-%d'),
        }
        
    def __init__(self, *args, **kwargs):
        actividad = kwargs.pop('actividad', None)
        super().__init__(*args, **kwargs)
        
        # Obtener la actividad relacionada (puede ser de una relación ForeignKey o algo similar)
        #actividad = getattr(self.instance, 'actividad', None)
        
        if actividad:
            # Configurar dinámicamente los límites de las fechas
            self.fields['fecha_inicio'].widget.attrs['min'] = actividad.fecha_inicio.isoformat()
            self.fields['fecha_inicio'].widget.attrs['max'] = actividad.fecha_fin.isoformat()
            self.fields['fecha_fin'].widget.attrs['min'] = actividad.fecha_inicio.isoformat()
            self.fields['fecha_fin'].widget.attrs['max'] = actividad.fecha_fin.isoformat()

# Formulario para contenido del Informe
class InformeContenidoForm(forms.ModelForm):
    class Meta:
        model = Informe
        fields = ['contenido']  # Solo incluye el campo 'contenido'
        labels = {
            'contenido': 'Contenido del Informe :',
        }
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
        }


# Formulario para Informe
class EvidenciaForm(forms.ModelForm):
    class Meta:
        model = Evidencia
        fields = ['imagen', 'archivo', 'enlace']
        labels = {
            'imagen': 'Evidencia de imagen:',
            'archivo': 'Evidencia de archivo (PDF u otros):',
            'enlace': 'Evidencia de enlace:',
        }
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'enlace': forms.URLInput(attrs={'class': 'form-control'}),
        }       

class UserManagementForm(forms.ModelForm):
    group = forms.ModelChoiceField(
        queryset=Group.objects.exclude(name="director"), 
        required=True,
        label="Rol",
        empty_label="Seleccione un rol"
    )
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email','group']
        labels = {
            'username': 'Nombre de usuario',
            'password': 'Contraseña',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
        }
        widgets = {
            #'username': forms.TextInput(attrs={'class': 'form-control-file','type':'number'}),
            
        }

class UserPerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']  # Solo los campos que necesitas
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
        }
        

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['img_usuario', 'img_firma']
        labels = {
            'img_usuario': 'Imagen de perfil',
            'img_firma': 'Firma (imagen)',
        }

