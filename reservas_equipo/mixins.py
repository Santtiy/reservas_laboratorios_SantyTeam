"""
Mixins personalizados para control de acceso basado en roles y permisos.

Responsable: Ronald (Feature: ronald-auth)
Descripción: Proporciona validación de roles y permisos en vistas.
"""

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured


# ============================================================================
# MIXINS DE ROLES
# ============================================================================

class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin genérico para validar que el usuario pertenece a uno o más grupos.
    
    Uso:
        class MiVista(RoleRequiredMixin, ListView):
            required_groups = ['Docente', 'Administrador']  # O solo uno
            model = Reserva
    
    Atributos:
        - required_groups: List[str] | str
            Lista de nombres de grupos permitidos
        - redirect_to: str
            URL a redirigir si no pasa validación (default: '/')
        - show_message: bool
            Si mostrar mensaje de error al usuario
    """
    
    required_groups = []
    redirect_to = 'home'
    show_message = True

    def dispatch(self, request, *args, **kwargs):
        """Intercepta la solicitud y valida permisos."""
        if not request.user.is_authenticated:
            return redirect('auth:login')
        
        if not self.test_func():
            if self.show_message:
                messages.error(
                    request,
                    '❌ No tienes permisos para acceder a esta sección.'
                )
            return redirect(self.redirect_to)
        
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        """
        Valida que el usuario pertenezca a uno de los grupos requeridos.
        """
        user = self.request.user
        
        # Permitir acceso a superusers
        if user.is_superuser:
            return True
        
        # Normalizar required_groups a lista
        groups = self.required_groups
        if isinstance(groups, str):
            groups = [groups]
        
        if not groups:
            raise ImproperlyConfigured(
                f'{self.__class__.__name__} debe definir required_groups'
            )
        
        # Verificar si el usuario pertenece a alguno de los grupos
        user_groups = user.groups.values_list('name', flat=True)
        return any(group in user_groups for group in groups)


class DoctenteMixin(RoleRequiredMixin):
    """
    Mixin para permitir solo a usuarios del grupo Docente.
    
    Validación automática: verifica que user.groups contiene 'Docente'
    """
    required_groups = 'Docente'


class AdministradorMixin(RoleRequiredMixin):
    """
    Mixin para permitir solo a usuarios del grupo Administrador.
    
    Validación automática: verifica que user.groups contiene 'Administrador'
    """
    required_groups = 'Administrador'


# ============================================================================
# MIXINS DE PROPIEDAD
# ============================================================================

class PropietarioReservaMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin que valida que el usuario sea propietario de la reserva.
    
    Uso:
        class ReservaUpdateView(PropietarioReservaMixin, UpdateView):
            model = Reserva
    
    Se asume que el objeto tiene un campo 'usuario' que apunta al propietario.
    Aplica también a Administradores (acceso total).
    """
    
    show_message = True

    def test_func(self):
        """
        Verifica:
        1. Usuario es superuser → acceso total
        2. Usuario es administrador → acceso total
        3. Usuario es propietario de la reserva → acceso
        4. Otro caso → rechaza
        """
        user = self.request.user
        obj = self.get_object()
        
        # Superusers siempre tienen acceso
        if user.is_superuser:
            return True
        
        # Administradores siempre tienen acceso
        if user.groups.filter(name='Administrador').exists():
            return True
        
        # Propietarios tienen acceso a su recurso
        if hasattr(obj, 'usuario'):
            return user == obj.usuario
        
        return False

    def handle_no_permission(self):
        """Personaliza el manejo de acceso denegado."""
        if self.show_message:
            messages.error(
                self.request,
                '❌ No tienes permiso para modificar esta reserva. '
                'Solo puedes editar tus propias reservas.'
            )
        return redirect('reservas:reserva_list')


class SoloAdministradorMixin(AdministradorMixin):
    """
    Restricción estricta: solo administradores, ni siquiera superusers sin el rol.
    Opcional: para casos muy específicos donde necesitas validación estricta.
    """
    
    def test_func(self):
        """No permite superusers, valida grupo específicamente."""
        user = self.request.user
        return user.groups.filter(name='Administrador').exists()


# ============================================================================
# MIXINS DE PERMISOS ESPECÍFICOS
# ============================================================================

class PermisionRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin genérico para validar permisos específicos de Django.
    
    Uso:
        class MiVista(PermisionRequiredMixin, ListView):
            required_permission = 'reservas_equipo.change_reserva'
            model = Reserva
    
    Soporta múltiples permisos (todos deben cumplirse):
        required_permission = [
            'reservas_equipo.add_reserva',
            'reservas_equipo.change_reserva',
        ]
    """
    
    required_permission = None
    redirect_to = 'home'
    show_message = True

    def dispatch(self, request, *args, **kwargs):
        """Intercepta y valida permisos."""
        if not request.user.is_authenticated:
            return redirect('auth:login')
        
        if not self.test_func():
            if self.show_message:
                messages.error(
                    request,
                    '❌ No tienes los permisos necesarios.'
                )
            return redirect(self.redirect_to)
        
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        """Valida que el usuario tenga los permisos requeridos."""
        user = self.request.user
        
        if user.is_superuser:
            return True
        
        if not self.required_permission:
            raise ImproperlyConfigured(
                f'{self.__class__.__name__} debe definir required_permission'
            )
        
        # Normalizar a lista
        permissions = self.required_permission
        if isinstance(permissions, str):
            permissions = [permissions]
        
        # Verificar todos los permisos
        return all(user.has_perm(perm) for perm in permissions)


# ============================================================================
# MIXIN DE AUDITORÍA (OPTIONAL)
# ============================================================================

class AuditoriaMixin:
    """
    Mixin para registrar quién realiza qué acción (OPCIONAL).
    
    Uso futuro:
        class ReservaUpdateView(AuditoriaMixin, UpdateView):
            model = Reserva
    
    Nota: Requiere modelo Auditoria para registrar cambios.
    """
    
    def form_valid(self, form):
        """Puede registrar cambios si necesitas auditoría."""
        # Aquí podrías registrar logs de cambios
        response = super().form_valid(form)
        # print(f"Usuario {self.request.user} modificó {self.object}")
        return response
