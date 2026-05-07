"""
URLs para la aplicación de reservas.
Responsable: Ronald (Feature: ronald-auth)

RUTAS:
- Docentes: crear, editar, eliminar PROPIAS reservas
- Administradores: ver todas, aprobar, rechazar reservas
"""
from django.urls import path
from reservas_equipo.views import (
    ReservaListView,
    ReservaDetailView,
    ReservaCreateView,
    ReservaUpdateView,
    ReservaDeleteView,
    ReservasAdministracionListView,
    AprobarReservaView,
    RechazarReservaView,
)

app_name = 'reservas'

urlpatterns = [
    # ========================================================================
    # RUTAS DOCENTE - Gestión de reservas propias
    # ========================================================================
    path(
        '',
        ReservaListView.as_view(),
        name='reserva_list'
    ),
    path(
        'nueva/',
        ReservaCreateView.as_view(),
        name='reserva_create'
    ),
    path(
        '<int:pk>/',
        ReservaDetailView.as_view(),
        name='reserva_detail'
    ),
    path(
        '<int:pk>/editar/',
        ReservaUpdateView.as_view(),
        name='reserva_update'
    ),
    path(
        '<int:pk>/eliminar/',
        ReservaDeleteView.as_view(),
        name='reserva_delete'
    ),
    
    # ========================================================================
    # RUTAS ADMINISTRADOR - Gestión de todas las reservas
    # ========================================================================
    path(
        'administracion/',
        ReservasAdministracionListView.as_view(),
        name='administracion_list'
    ),
    path(
        '<int:pk>/aprobar/',
        AprobarReservaView.as_view(),
        name='reserva_aprobar'
    ),
    path(
        '<int:pk>/rechazar/',
        RechazarReservaView.as_view(),
        name='reserva_rechazar'
    ),
]
