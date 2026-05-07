from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from datetime import datetime, timedelta

from .models import Reserva, Laboratorio
from .forms import ReservaForm, LoginCustomForm, FiltroReservasForm


# ============================================================================
# VISTAS DE AUTENTICACIÓN
# ============================================================================

class LoginView(LoginView):
    """
    Vista de login personalizada.
    Utiliza formulario personalizado con Bootstrap.
    """
    form_class = LoginCustomForm
    template_name = 'auth/login.html'
    redirect_authenticated_user = True


class LogoutView(LogoutView):
    """
    Vista de logout que redirige al home.
    """
    next_page = reverse_lazy('home')


# ============================================================================
# VISTAS DE RESERVAS
# ============================================================================

class HomeView(TemplateView):
    """
    Vista de inicio del sistema.
    Muestra información general y acceso a funcionalidades.
    """
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            # Estadísticas básicas para el usuario logueado
            context['total_reservas'] = Reserva.objects.filter(
                usuario=self.request.user
            ).count()
            context['reservas_pendientes'] = Reserva.objects.filter(
                usuario=self.request.user,
                estado='pendiente'
            ).count()
            context['proximas_reservas'] = Reserva.objects.filter(
                usuario=self.request.user,
                fecha__gte=datetime.now().date(),
                estado='aprobada'
            ).order_by('fecha', 'hora_inicio')[:5]
        
        return context


class ReservaListView(LoginRequiredMixin, ListView):
    """
    Vista que lista todas las reservas del usuario actual.
    Soporta filtros básicos.
    
    Accesible desde: /reservas/
    """
    model = Reserva
    template_name = 'reservas/reserva_list.html'
    context_object_name = 'reservas'
    paginate_by = 10

    def get_queryset(self):
        """
        Retorna las reservas del usuario actual.
        Puede ser filtrado si se implementan funcionalidades admin.
        """
        queryset = Reserva.objects.filter(usuario=self.request.user).select_related(
            'laboratorio', 'usuario'
        )
        
        # Implementar filtros aquí (será tarea de algún miembro del equipo)
        laboratorio_id = self.request.GET.get('laboratorio')
        estado = self.request.GET.get('estado')
        
        if laboratorio_id:
            queryset = queryset.filter(laboratorio_id=laboratorio_id)
        
        if estado:
            queryset = queryset.filter(estado=estado)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_filtro'] = FiltroReservasForm(self.request.GET)
        context['laboratorios'] = Laboratorio.objects.filter(activo=True)
        return context


class ReservaDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Vista de detalle de una reserva.
    Solo el creador puede verla.
    
    Accesible desde: /reservas/<id>/
    """
    model = Reserva
    template_name = 'reservas/reserva_detail.html'
    context_object_name = 'reserva'

    def test_func(self):
        """Verifica que el usuario sea el propietario de la reserva."""
        reserva = self.get_object()
        return self.request.user == reserva.usuario or self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para ver esta reserva.')
        return redirect('reserva_list')


class ReservaCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para crear una nueva reserva.
    
    Accesible desde: /reservas/nueva/
    """
    model = Reserva
    form_class = ReservaForm
    template_name = 'reservas/reserva_form.html'
    success_url = reverse_lazy('reserva_list')

    def form_valid(self, form):
        """Asocia automáticamente el usuario actual a la reserva."""
        form.instance.usuario = self.request.user
        messages.success(
            self.request,
            '✓ Reserva creada exitosamente. Está pendiente de aprobación.'
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nueva Reserva'
        context['boton'] = 'Crear Reserva'
        return context


class ReservaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Vista para editar una reserva existente.
    Solo se puede editar si está en estado 'pendiente'.
    
    Accesible desde: /reservas/<id>/editar/
    """
    model = Reserva
    form_class = ReservaForm
    template_name = 'reservas/reserva_form.html'
    success_url = reverse_lazy('reserva_list')

    def test_func(self):
        """
        Verifica que:
        1. El usuario sea el propietario
        2. La reserva esté en estado 'pendiente'
        """
        reserva = self.get_object()
        return (
            self.request.user == reserva.usuario and
            reserva.estado == 'pendiente'
        )

    def handle_no_permission(self):
        messages.error(
            self.request,
            'Solo puedes editar reservas pendientes que te pertenecen.'
        )
        return redirect('reserva_list')

    def form_valid(self, form):
        messages.success(self.request, '✓ Reserva actualizada exitosamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Reserva'
        context['boton'] = 'Guardar Cambios'
        return context


class ReservaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Vista para eliminar una reserva.
    Solo se puede eliminar si está en estado 'pendiente'.
    
    Accesible desde: /reservas/<id>/eliminar/
    """
    model = Reserva
    template_name = 'reservas/reserva_confirm_delete.html'
    success_url = reverse_lazy('reserva_list')

    def test_func(self):
        """
        Verifica que:
        1. El usuario sea el propietario
        2. La reserva esté en estado 'pendiente'
        """
        reserva = self.get_object()
        return (
            self.request.user == reserva.usuario and
            reserva.estado == 'pendiente'
        )

    def handle_no_permission(self):
        messages.error(
            self.request,
            'Solo puedes eliminar reservas pendientes que te pertenecen.'
        )
        return redirect('reserva_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, '✓ Reserva eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)
