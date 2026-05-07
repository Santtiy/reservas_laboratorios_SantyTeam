from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class Laboratorio(models.Model):
    """
    Modelo para representar los laboratorios disponibles.
    Base para futuras funcionalidades de gestión de laboratorios.
    """
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    capacidad = models.IntegerField(default=1)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Laboratorio"
        verbose_name_plural = "Laboratorios"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Reserva(models.Model):
    """
    Modelo principal para las reservas de laboratorios.
    Incluye validación básica de conflictos horarios.
    """
    
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    )

    # Campos principales
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.PROTECT, related_name='reservas')
    
    # Información de la reserva
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    
    # Datos administrativos
    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default='pendiente'
    )
    motivo = models.TextField(help_text="Descripción del uso del laboratorio")
    
    # Metadata
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-fecha', 'hora_inicio']
        # unique_together removed to allow overlapping checks via business logic

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.laboratorio} - {self.fecha}"

    def clean(self):
        """Validación de la integridad de la reserva."""
        # Validar que hora_fin > hora_inicio
        if self.hora_fin <= self.hora_inicio:
            raise ValidationError("La hora de fin debe ser mayor a la hora de inicio.")
        
        # Validar que no sea una fecha pasada
        if self.fecha < timezone.now().date() and self.pk is None:
            raise ValidationError("No puedes reservar para fechas pasadas.")

        # Validar solapamiento de reservas: mismo laboratorio y misma fecha
        if self.laboratorio and self.fecha and self.hora_inicio and self.hora_fin:
            conflictos = Reserva.objects.filter(
                laboratorio=self.laboratorio,
                fecha=self.fecha
            ).exclude(pk=self.pk)

            for otro in conflictos:
                # Existe solapamiento si inicio < otro.hora_fin and fin > otro.hora_inicio
                if (self.hora_inicio < otro.hora_fin) and (self.hora_fin > otro.hora_inicio):
                    msg = (
                        f"Conflicto de horario con reserva existente: "
                        f"{otro.usuario.get_full_name() or otro.usuario.username} "
                        f"({otro.hora_inicio} - {otro.hora_fin})"
                    )
                    raise ValidationError(msg)

    def save(self, *args, **kwargs):
        """Ejecuta validaciones antes de guardar."""
        self.full_clean()
        super().save(*args, **kwargs)

    def get_estado_display_badge(self):
        """Retorna una clase CSS para el badge según el estado."""
        badges = {
            'pendiente': 'warning',
            'aprobada': 'success',
            'rechazada': 'danger',
        }
        return badges.get(self.estado, 'secondary')
