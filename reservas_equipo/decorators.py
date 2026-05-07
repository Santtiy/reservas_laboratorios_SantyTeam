"""
Decoradores personalizados para validación de roles y permisos.

Responsable: Ronald (Feature: ronald-auth)
Descripción: Decoradores para vistas basadas en funciones (FBV) si es necesario.

Nota: Se prefiere usar CBV con Mixins, pero estos decoradores están disponibles
para casos especiales.
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


# ============================================================================
# DECORADORES DE ROLES
# ============================================================================

def role_required(role_name):
    """
    Decorador para verificar que el usuario pertenece a un rol específico.
    
    Uso:
        @role_required('Docente')
        def mi_vista(request):
            return render(request, 'template.html')
    
    Args:
        role_name (str): Nombre del grupo/rol requerido
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='auth:login')
        def wrapper(request, *args, **kwargs):
            # Permitir a superusers
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Verificar si el usuario pertenece al grupo
            if request.user.groups.filter(name=role_name).exists():
                return view_func(request, *args, **kwargs)
            
            # Si no tiene el rol, mostrar error
            messages.error(
                request,
                f'❌ Acceso denegado. Se requiere el rol: {role_name}'
            )
            return redirect('home')
        
        return wrapper
    return decorator


def roles_required(*role_names):
    """
    Decorador para verificar que el usuario pertenece a CUALQUIERA de los roles especificados.
    
    Uso:
        @roles_required('Docente', 'Administrador')
        def mi_vista(request):
            return render(request, 'template.html')
    
    Args:
        *role_names: Nombres de roles permitidos
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='auth:login')
        def wrapper(request, *args, **kwargs):
            # Permitir a superusers
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Verificar si el usuario pertenece a alguno de los grupos
            user_groups = request.user.groups.values_list('name', flat=True)
            if any(role in user_groups for role in role_names):
                return view_func(request, *args, **kwargs)
            
            # Si no tiene ninguno de los roles
            messages.error(
                request,
                f'❌ Acceso denegado. Se requiere uno de los siguientes roles: {", ".join(role_names)}'
            )
            return redirect('home')
        
        return wrapper
    return decorator


def docente_required(view_func):
    """
    Decorador específico para verificar el rol Docente.
    Equivalente a @role_required('Docente')
    """
    return role_required('Docente')(view_func)


def administrador_required(view_func):
    """
    Decorador específico para verificar el rol Administrador.
    Equivalente a @role_required('Administrador')
    """
    return role_required('Administrador')(view_func)


# ============================================================================
# DECORADORES DE PERMISOS
# ============================================================================

def permission_required(perm):
    """
    Decorador para verificar un permiso específico de Django.
    
    Uso:
        @permission_required('reservas_equipo.add_reserva')
        def crear_reserva(request):
            return render(request, 'form.html')
    
    Args:
        perm (str): Permiso en formato 'app.codename'
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='auth:login')
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            if request.user.has_perm(perm):
                return view_func(request, *args, **kwargs)
            
            messages.error(
                request,
                '❌ No tienes los permisos necesarios para acceder a esta sección.'
            )
            return redirect('home')
        
        return wrapper
    return decorator


# ============================================================================
# DECORADORES DE PROPIEDAD
# ============================================================================

def propietario_required(model_class):
    """
    Decorador para verificar que el usuario es propietario del objeto.
    
    Uso:
        @propietario_required(Reserva)
        def editar_reserva(request, pk):
            reserva = Reserva.objects.get(pk=pk)
            return render(request, 'form.html', {'reserva': reserva})
    
    Args:
        model_class: Clase del modelo (ej: Reserva)
    
    Nota: El objeto debe tener un campo 'usuario' que apunte al propietario
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='auth:login')
        def wrapper(request, *args, **kwargs):
            # Obtener el pk del objeto
            pk = kwargs.get('pk')
            if not pk:
                messages.error(request, '❌ Objeto no encontrado.')
                return redirect('home')
            
            try:
                obj = model_class.objects.get(pk=pk)
            except model_class.DoesNotExist:
                messages.error(request, '❌ Objeto no encontrado.')
                return redirect('home')
            
            # Verificar propiedad
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            if request.user.groups.filter(name='Administrador').exists():
                return view_func(request, *args, **kwargs)
            
            if hasattr(obj, 'usuario') and request.user == obj.usuario:
                return view_func(request, *args, **kwargs)
            
            messages.error(
                request,
                '❌ No tienes permiso para acceder a este objeto.'
            )
            return redirect('home')
        
        return wrapper
    return decorator
