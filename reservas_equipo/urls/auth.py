"""
URLs para la aplicación de autenticación.
Integrante responsable: [Módulo de Autenticación]
"""
from django.urls import path
from django.contrib.auth.views import LogoutView
from reservas_equipo.views import LoginView

app_name = 'auth'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]
