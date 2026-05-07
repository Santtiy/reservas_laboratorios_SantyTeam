"""
Data migration para crear grupos de usuarios y asignar permisos.

Responsable: Ronald (Feature: ronald-auth)
Descripción: Crea dos grupos:
    - Docente: puede crear, editar, eliminar propias reservas
    - Administrador: puede ver, aprobar, rechazar todas las reservas
"""

from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


def create_groups_and_permissions(apps, schema_editor):
    """
    Crea los grupos Docente y Administrador con sus permisos respectivos.
    """
    
    # Obtener ContentType del modelo Reserva
    reserva_content_type = ContentType.objects.get(
        app_label='reservas_equipo',
        model='reserva'
    )
    
    # ========================================================================
    # GRUPO: DOCENTE
    # ========================================================================
    docente_group, _ = Group.objects.get_or_create(name='Docente')
    
    # Permisos para Docente
    docente_permisos = [
        'add_reserva',      # Crear reservas
        'change_reserva',   # Editar reservas propias
        'delete_reserva',   # Eliminar reservas propias
    ]
    
    for permiso_codename in docente_permisos:
        try:
            permiso = Permission.objects.get(
                content_type=reserva_content_type,
                codename=permiso_codename
            )
            docente_group.permissions.add(permiso)
        except Permission.DoesNotExist:
            print(f"⚠️ Permiso {permiso_codename} no encontrado")
    
    print(f"✅ Grupo Docente creado con {docente_group.permissions.count()} permisos")
    
    # ========================================================================
    # GRUPO: ADMINISTRADOR
    # ========================================================================
    admin_group, _ = Group.objects.get_or_create(name='Administrador')
    
    # Permisos para Administrador
    admin_permisos = [
        'add_reserva',
        'change_reserva',   # Editar cualquier reserva (aprobar/rechazar)
        'delete_reserva',
        'view_reserva',     # Ver detalles de reservas
    ]
    
    for permiso_codename in admin_permisos:
        try:
            permiso = Permission.objects.get(
                content_type=reserva_content_type,
                codename=permiso_codename
            )
            admin_group.permissions.add(permiso)
        except Permission.DoesNotExist:
            print(f"⚠️ Permiso {permiso_codename} no encontrado")
    
    print(f"✅ Grupo Administrador creado con {admin_group.permissions.count()} permisos")
    print("✅ MIGRACIÓN COMPLETADA: Grupos y permisos asignados correctamente")


def delete_groups_and_permissions(apps, schema_editor):
    """
    Revierte la migración eliminando los grupos.
    """
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['Docente', 'Administrador']).delete()
    print("✅ Grupos eliminados correctamente")


class Migration(migrations.Migration):

    dependencies = [
        ('reservas_equipo', '0001_initial'),  # Asegúrate de que esta es la migración anterior
    ]

    operations = [
        migrations.RunPython(create_groups_and_permissions, delete_groups_and_permissions),
    ]
