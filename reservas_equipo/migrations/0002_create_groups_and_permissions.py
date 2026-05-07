"""
Data migration para crear grupos de usuarios y asignar permisos.

Responsable: Ronald (Feature: ronald-auth)
Descripción: Crea dos grupos:
    - Docente: puede crear, editar, eliminar propias reservas
    - Administrador: puede ver, aprobar, rechazar todas las reservas
"""

from django.db import migrations


def create_groups_and_permissions(apps, schema_editor):
    """
    Crea los grupos Docente y Administrador con sus permisos respectivos.
    """
    
    # Obtener modelos usando apps para compatibilidad con migraciones
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    
    # Obtener o crear ContentType para Reserva
    try:
        reserva_ct = ContentType.objects.get(app_label='reservas_equipo', model='reserva')
    except ContentType.DoesNotExist:
        # Si no existe, crear uno
        reserva_ct = ContentType.objects.create(
            app_label='reservas_equipo',
            model='reserva'
        )
    
    # ========================================================================
    # GRUPO: DOCENTE
    # ========================================================================
    docente_group, _ = Group.objects.get_or_create(name='Docente')
    
    # Permisos para Docente: add, change, delete para Reserva
    docente_permisos = Permission.objects.filter(
        content_type=reserva_ct,
        codename__in=['add_reserva', 'change_reserva', 'delete_reserva']
    )
    
    for permiso in docente_permisos:
        docente_group.permissions.add(permiso)
    
    print(f"✅ Grupo Docente creado con {docente_group.permissions.count()} permisos")
    
    # ========================================================================
    # GRUPO: ADMINISTRADOR
    # ========================================================================
    admin_group, _ = Group.objects.get_or_create(name='Administrador')
    
    # Permisos para Administrador: add, change, delete, view para Reserva
    admin_permisos = Permission.objects.filter(
        content_type=reserva_ct,
        codename__in=['add_reserva', 'change_reserva', 'delete_reserva', 'view_reserva']
    )
    
    for permiso in admin_permisos:
        admin_group.permissions.add(permiso)
    
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
