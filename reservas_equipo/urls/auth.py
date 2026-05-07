"""
URLs para la aplicación de autenticación.
Integrante responsable: [Módulo de Autenticación]
"""
from django.urls import path
from reservas_equipo.views import LoginView, LogoutView

app_name = 'auth'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
