"""
URLs para la aplicación de reservas.
Integrante responsable: [Módulo de Reservas]
"""
from django.urls import path
from reservas_equipo.views import (
    ReservaListView,
    ReservaDetailView,
    ReservaCreateView,
    ReservaUpdateView,
    ReservaDeleteView,
)

app_name = 'reservas'

urlpatterns = [
    # Listado de reservas
    path('', ReservaListView.as_view(), name='reserva_list'),
    
    # CRUD de reservas
    path('nueva/', ReservaCreateView.as_view(), name='reserva_create'),
    path('<int:pk>/', ReservaDetailView.as_view(), name='reserva_detail'),
    path('<int:pk>/editar/', ReservaUpdateView.as_view(), name='reserva_update'),
    path('<int:pk>/eliminar/', ReservaDeleteView.as_view(), name='reserva_delete'),
]
