import csv
from django.db.models import Count
from django.utils import timezone
from .models import Reserva, Laboratorio
from collections import Counter

def generar_estadisticas(queryset):
    """
    Genera las estadísticas (cantidad, labs más usados, estado) a partir del queryset filtrado.
    """
    total_reservas = queryset.count()
    
    # Reservas por estado
    estado_counts = queryset.values('estado').annotate(total=Count('id')).order_by('-total')
    estadisticas_estado = {item['estado']: item['total'] for item in estado_counts}

    # Laboratorios más usados
    lab_counts = queryset.values('laboratorio__nombre').annotate(total=Count('id')).order_by('-total')[:5]
    laboratorios_mas_usados = [{'laboratorio': item['laboratorio__nombre'], 'total': item['total']} for item in lab_counts]

    return {
        'total_reservas': total_reservas,
        'reservas_por_estado': estadisticas_estado,
        'laboratorios_mas_usados': laboratorios_mas_usados,
    }

def generar_csv_reservas(queryset, response):
    """
    Exporta el queryset de reservas a CSV directamente en la respuesta (HttpResponse).
    """
    writer = csv.writer(response)
    writer.writerow([
        'ID Reserva',
        'Usuario',
        'Laboratorio',
        'Fecha',
        'Hora Inicio',
        'Hora Fin',
        'Estado',
        'Motivo',
        'Fecha de Alta'
    ])
    
    for reserva in queryset:
        writer.writerow([
            reserva.id,
            reserva.usuario.get_full_name() or reserva.usuario.username,
            reserva.laboratorio.nombre,
            reserva.fecha.strftime('%Y-%m-%d'),
            reserva.hora_inicio.strftime('%H:%M:%S'),
            reserva.hora_fin.strftime('%H:%M:%S'),
            reserva.get_estado_display(),
            reserva.motivo,
            reserva.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')
        ])

def obtener_reservas_filtradas(fecha_inicio=None, fecha_fin=None, laboratorio_id=None, estado=None):
    """
    Filtra las reservas centralizadamente.
    """
    queryset = Reserva.objects.all().select_related('laboratorio', 'usuario')

    if fecha_inicio:
        queryset = queryset.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        queryset = queryset.filter(fecha__lte=fecha_fin)
    if laboratorio_id:
        queryset = queryset.filter(laboratorio_id=laboratorio_id)
    if estado:
        queryset = queryset.filter(estado=estado)
        
    return queryset
