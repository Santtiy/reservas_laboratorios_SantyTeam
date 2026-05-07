from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from datetime import datetime, timedelta

from .models import Reserva, Laboratorio
from .forms import ReservaForm, LoginCustomForm, FiltroReservasForm
from .mixins import (
    DoctenteMixin,
    AdministradorMixin,
    PropietarioReservaMixin,
    RoleRequiredMixin
)


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


class ReservaCreateView(DoctenteMixin, CreateView):
    """
    Vista para crear una nueva reserva.
    SOLO accesible para usuarios del grupo Docente.
    
    Accesible desde: /reservas/nueva/
    
    Validación:
    - Usuario debe estar autenticado
    - Usuario debe ser Docente
    - Automáticamente asocia el usuario actual a la reserva
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


class ReservaUpdateView(DoctenteMixin, PropietarioReservaMixin, UpdateView):
    """
    Vista para editar una reserva existente.
    SOLO accesible para:
    - Usuario Docente que es propietario de la reserva
    - Usuario Administrador
    
    Solo se puede editar si está en estado 'pendiente'.
    
    Accesible desde: /reservas/<id>/editar/
    
    Validaciones:
    1. Usuario debe ser Docente (DoctenteMixin)
    2. Usuario debe ser propietario o Administrador (PropietarioReservaMixin)
    3. Reserva debe estar en estado 'pendiente'
    """
    model = Reserva
    form_class = ReservaForm
    template_name = 'reservas/reserva_form.html'
    success_url = reverse_lazy('reserva_list')

    def test_func(self):
        """
        Valida que la reserva esté en estado 'pendiente'.
        La propiedad ya la valida PropietarioReservaMixin.
        """
        reserva = self.get_object()
        
        # Primero valida propietario
        if not super().test_func():
            return False
        
        # Luego valida estado
        if reserva.estado != 'pendiente':
            messages.error(
                self.request,
                '❌ Solo puedes editar reservas en estado pendiente.'
            )
            return False
        
        return True

    def form_valid(self, form):
        messages.success(self.request, '✓ Reserva actualizada exitosamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Reserva'
        context['boton'] = 'Guardar Cambios'
        return context


class ReservaDeleteView(DoctenteMixin, PropietarioReservaMixin, DeleteView):
    """
    Vista para eliminar una reserva.
    SOLO accesible para:
    - Usuario Docente que es propietario de la reserva
    - Usuario Administrador
    
    Solo se puede eliminar si está en estado 'pendiente'.
    
    Accesible desde: /reservas/<id>/eliminar/
    
    Validaciones:
    1. Usuario debe ser Docente (DoctenteMixin)
    2. Usuario debe ser propietario o Administrador (PropietarioReservaMixin)
    3. Reserva debe estar en estado 'pendiente'
    """
    model = Reserva
    template_name = 'reservas/reserva_confirm_delete.html'
    success_url = reverse_lazy('reserva_list')

    def test_func(self):
        """
        Valida que la reserva esté en estado 'pendiente'.
        La propiedad ya la valida PropietarioReservaMixin.
        """
        reserva = self.get_object()
        
        # Primero valida propietario
        if not super().test_func():
            return False
        
        # Luego valida estado
        if reserva.estado != 'pendiente':
            messages.error(
                self.request,
                '❌ Solo puedes eliminar reservas en estado pendiente.'
            )
            return False
        
        return True

    def delete(self, request, *args, **kwargs):
        messages.success(request, '✓ Reserva eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# VISTAS DE ADMINISTRACIÓN (SOLO ADMINISTRADORES)
# ============================================================================

class ReservasAdministracionListView(AdministradorMixin, ListView):
    """
    Vista que lista TODAS las reservas del sistema (solo Administradores).
    SOLO accesible para usuarios del grupo Administrador.
    
    Accesible desde: /reservas/administracion/
    
    Funcionalidades:
    - Ver todas las reservas del sistema (no filtradas por usuario)
    - Filtrar por estado (pendiente, aprobada, rechazada)
    - Filtrar por laboratorio
    - Acceder a detalles para aprobar/rechazar
    """
    model = Reserva
    template_name = 'reservas/reserva_administracion_list.html'
    context_object_name = 'reservas'
    paginate_by = 20

    def get_queryset(self):
        """
        Retorna TODAS las reservas del sistema (no filtradas por usuario).
        Soporta filtros por estado y laboratorio.
        """
        queryset = Reserva.objects.select_related('laboratorio', 'usuario')
        
        # Filtro por estado
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        
        # Filtro por laboratorio
        laboratorio_id = self.request.GET.get('laboratorio')
        if laboratorio_id:
            queryset = queryset.filter(laboratorio_id=laboratorio_id)
        
        # Ordenar por fecha descendente
        queryset = queryset.order_by('-fecha', 'hora_inicio')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['laboratorios'] = Laboratorio.objects.filter(activo=True)
        context['estados'] = Reserva.ESTADO_CHOICES
        context['estado_filtro'] = self.request.GET.get('estado', '')
        return context


class AprobarReservaView(AdministradorMixin, DetailView):
    """
    Vista para aprobar una reserva (solo Administradores).
    
    Accesible desde: /reservas/<id>/aprobar/
    
    Funcionalidades:
    - Cambia estado de 'pendiente' a 'aprobada'
    - Envía notificación al usuario (opcional futura)
    - Redirige a lista de administración
    """
    model = Reserva
    template_name = 'reservas/reserva_detail.html'
    context_object_name = 'reserva'

    def post(self, request, *args, **kwargs):
        """Procesa la aprobación de la reserva."""
        reserva = self.get_object()
        
        # Validar que esté en estado pendiente
        if reserva.estado != 'pendiente':
            messages.error(
                request,
                f'❌ No se puede aprobar una reserva en estado {reserva.get_estado_display().lower()}.'
            )
            return redirect('reservas:reserva_detail', pk=reserva.pk)
        
        # Cambiar estado
        reserva.estado = 'aprobada'
        reserva.save()
        
        messages.success(
            request,
            f'✅ Reserva de {reserva.usuario.get_full_name()} aprobada correctamente.'
        )
        return redirect('reservas:administracion_list')

    def get(self, request, *args, **kwargs):
        """GET redirige, solo POST es válido."""
        return self.post(request, *args, **kwargs)


class RechazarReservaView(AdministradorMixin, DetailView):
    """
    Vista para rechazar una reserva (solo Administradores).
    
    Accesible desde: /reservas/<id>/rechazar/
    
    Funcionalidades:
    - Cambia estado de 'pendiente' a 'rechazada'
    - Envía notificación al usuario (opcional futura)
    - Redirige a lista de administración
    """
    model = Reserva
    template_name = 'reservas/reserva_detail.html'
    context_object_name = 'reserva'

    def post(self, request, *args, **kwargs):
        """Procesa el rechazo de la reserva."""
        reserva = self.get_object()
        
        # Validar que esté en estado pendiente
        if reserva.estado != 'pendiente':
            messages.error(
                request,
                f'❌ No se puede rechazar una reserva en estado {reserva.get_estado_display().lower()}.'
            )
            return redirect('reservas:reserva_detail', pk=reserva.pk)
        
        # Cambiar estado
        reserva.estado = 'rechazada'
        reserva.save()
        
        messages.success(
            request,
            f'❌ Reserva de {reserva.usuario.get_full_name()} rechazada correctamente.'
        )
        return redirect('reservas:administracion_list')

    def get(self, request, *args, **kwargs):
        """GET redirige, solo POST es válido."""
        return self.post(request, *args, **kwargs)

from django.http import HttpResponse
from .reportes import generar_estadisticas, generar_csv_reservas, obtener_reservas_filtradas

class ReportesView(AdministradorMixin, TemplateView):
    """
    Vista para visualización de estadísticas y generación de reportes.
    Accesible solo para Administradores.
    """
    template_name = 'reportes/reportes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener Filtros
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')
        laboratorio_id = self.request.GET.get('laboratorio')
        estado = self.request.GET.get('estado')

        # Obtener queryset filtrado centralizadamente
        queryset = obtener_reservas_filtradas(fecha_inicio, fecha_fin, laboratorio_id, estado)
        
        # Generar estadísticas
        context['estadisticas'] = generar_estadisticas(queryset)
        context['laboratorios'] = Laboratorio.objects.all()
        context['estados'] = Reserva.ESTADO_CHOICES
        context['reservas_list'] = queryset[:50]  # Limite para la tabla de visualización
        
        # Pasar valores de filtro al template para mantener estado
        context['filtros'] = {
            'fecha_inicio': fecha_inicio or '',
            'fecha_fin': fecha_fin or '',
            'laboratorio': int(laboratorio_id) if laboratorio_id and laboratorio_id.isdigit() else '',
            'estado': estado or '',
            'query_string': self.request.GET.urlencode(),
        }
        
        return context

class ExportarCSVView(AdministradorMixin, View):
    """
    Vista para exportar la lista filtrada a CSV.
    """
    def get(self, request, *args, **kwargs):
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')
        laboratorio_id = self.request.GET.get('laboratorio')
        estado = self.request.GET.get('estado')

        queryset = obtener_reservas_filtradas(fecha_inicio, fecha_fin, laboratorio_id, estado)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="reporte_reservas_{datetime.now().strftime("%Y%m%d_%H%M")}.csv"'
        
        generar_csv_reservas(queryset, response)
        
        return response

