from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Reserva, Laboratorio


class ReservaForm(forms.ModelForm):
    """
    Formulario para crear y editar reservas.
    Incluye validaciones básicas de horarios.
    """
    
    class Meta:
        model = Reserva
        fields = ['laboratorio', 'fecha', 'hora_inicio', 'hora_fin', 'motivo']
        widgets = {
            'laboratorio': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'required': True
            }),
            'hora_inicio': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
                'required': True
            }),
            'hora_fin': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
                'required': True
            }),
            'motivo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe para qué necesitas el laboratorio',
                'required': True
            }),
        }

    def clean(self):
        """Validación adicional del formulario."""
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')

        if hora_inicio and hora_fin:
            if hora_fin <= hora_inicio:
                self.add_error(
                    'hora_fin',
                    'La hora de fin debe ser mayor a la hora de inicio'
                )

        # Propagar validaciones del modelo (ej. solapamientos)
        laboratorio = cleaned_data.get('laboratorio')
        fecha = cleaned_data.get('fecha')

        # Preparar instancia temporal para validar reglas de negocio
        try:
            # Asignar valores a la instancia para que model.clean() pueda usarlos
            self.instance.laboratorio = laboratorio
            self.instance.fecha = fecha
            self.instance.hora_inicio = hora_inicio
            self.instance.hora_fin = hora_fin

            # Llamar a clean() del modelo para detectar solapamientos
            self.instance.clean()
        except Exception as e:
            # Si es ValidationError del modelo, agregar errores al formulario
            from django.core.exceptions import ValidationError

            if isinstance(e, ValidationError):
                # Agregar como error no-field o en campos según corresponda
                msg = e.message if hasattr(e, 'message') else e.messages
                # Si es dict, propagar por campos
                if hasattr(e, 'error_dict') and e.error_dict:
                    for field, errors in e.error_dict.items():
                        for er in errors:
                            self.add_error(field, er)
                else:
                    # Agregar a non_field_errors
                    self.add_error(None, msg)
            else:
                # Errores inesperados deben volver a lanzarse
                raise

        return cleaned_data


class LoginCustomForm(AuthenticationForm):
    """
    Formulario de autenticación personalizado con estilos Bootstrap.
    """
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )


class FiltroReservasForm(forms.Form):
    """
    Formulario para filtrar reservas en el listado.
    Será usado por la vista ListView.
    """
    laboratorio = forms.ModelChoiceField(
        queryset=Laboratorio.objects.filter(activo=True),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        })
    )
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        })
    )
    estado = forms.ChoiceField(
        choices=[('', '-- Todos los estados --')] + list(Reserva.ESTADO_CHOICES),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
