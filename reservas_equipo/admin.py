from django.contrib import admin
from django.utils.html import format_html
from .models import Laboratorio, Reserva


@admin.register(Laboratorio)
class LaboratorioAdmin(admin.ModelAdmin):
    """
    Administración de Laboratorios.
    Responsable: [Módulo de Administración]
    """
    list_display = ('nombre', 'capacidad', 'estado_badge', 'fecha_creacion')
    list_filter = ('activo', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)
    
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'descripcion', 'capacidad')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )
    
    def estado_badge(self, obj):
        """Muestra el estado del laboratorio como badge."""
        if obj.activo:
            return format_html(
                '<span style="background-color: #198754; color: white; padding: 5px 10px; border-radius: 3px;">Activo</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 5px 10px; border-radius: 3px;">Inactivo</span>'
        )
    estado_badge.short_description = 'Estado'


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    """
    Administración de Reservas.
    Responsable: [Módulo de Administración]
    """
    list_display = (
        'id', 'usuario_display', 'laboratorio', 'fecha', 
        'hora_inicio', 'hora_fin', 'estado_badge', 'fecha_creacion'
    )
    list_filter = ('estado', 'fecha', 'laboratorio', 'fecha_creacion')
    search_fields = ('usuario__username', 'usuario__first_name', 'laboratorio__nombre', 'motivo')
    ordering = ('-fecha', '-hora_inicio')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    
    fieldsets = (
        ('Información de la Reserva', {
            'fields': ('usuario', 'laboratorio', 'fecha')
        }),
        ('Horario', {
            'fields': ('hora_inicio', 'hora_fin')
        }),
        ('Detalles', {
            'fields': ('motivo', 'estado')
        }),
        ('Metadata', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def usuario_display(self, obj):
        """Muestra el nombre completo del usuario."""
        return obj.usuario.get_full_name() or obj.usuario.username
    usuario_display.short_description = 'Usuario'
    
    def estado_badge(self, obj):
        """Muestra el estado de la reserva como badge."""
        colors = {
            'pendiente': '#ffc107',
            'aprobada': '#198754',
            'rechazada': '#dc3545',
        }
        color = colors.get(obj.estado, '#6c757d')
        
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 5px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            'black' if obj.estado == 'pendiente' else 'white',
            obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'
    
    def save_model(self, request, obj, form, change):
        """Guarda el modelo."""
        super().save_model(request, obj, form, change)

