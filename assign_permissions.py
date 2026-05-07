"""
Script para asignar permisos a los grupos después de la migración.
"""

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from reservas_equipo.models import Reserva

print("\n" + "="*70)
print("ASIGNANDO PERMISOS A GRUPOS")
print("="*70 + "\n")

try:
    # Obtener ContentType de Reserva
    reserva_ct = ContentType.objects.get_for_model(Reserva)
    print(f"✅ ContentType encontrado: {reserva_ct}")
    
    # Obtener grupos
    docente = Group.objects.get(name='Docente')
    admin = Group.objects.get(name='Administrador')
    print(f"✅ Grupos encontrados: Docente, Administrador")
    
    # Obtener permisos disponibles
    add_perm = Permission.objects.get(content_type=reserva_ct, codename='add_reserva')
    change_perm = Permission.objects.get(content_type=reserva_ct, codename='change_reserva')
    delete_perm = Permission.objects.get(content_type=reserva_ct, codename='delete_reserva')
    view_perm = Permission.objects.get(content_type=reserva_ct, codename='view_reserva')
    print(f"✅ Permisos encontrados: add, change, delete, view")
    
    # Asignar a Docente
    docente.permissions.add(add_perm, change_perm, delete_perm)
    print(f"\n📋 Grupo DOCENTE:")
    print(f"   ✅ add_reserva")
    print(f"   ✅ change_reserva")
    print(f"   ✅ delete_reserva")
    print(f"   Total: {docente.permissions.count()} permisos")
    
    # Asignar a Administrador
    admin.permissions.add(add_perm, change_perm, delete_perm, view_perm)
    print(f"\n📋 Grupo ADMINISTRADOR:")
    print(f"   ✅ add_reserva")
    print(f"   ✅ change_reserva")
    print(f"   ✅ delete_reserva")
    print(f"   ✅ view_reserva")
    print(f"   Total: {admin.permissions.count()} permisos")
    
    print("\n" + "="*70)
    print("✅ PERMISOS ASIGNADOS CORRECTAMENTE")
    print("="*70 + "\n")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
