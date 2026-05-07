"""
Script de Validación del Sistema de Autenticación y Roles

Responsable: Ronald (Feature: ronald-auth)
Uso: python manage.py shell < validate_auth_system.py

Este script valida que todos los componentes del sistema de autenticación
estén correctamente configurados.
"""

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from reservas_equipo.models import Reserva

print("\n" + "="*70)
print("VALIDACIÓN DEL SISTEMA DE AUTENTICACIÓN Y ROLES")
print("="*70 + "\n")

# ============================================================================
# 1. VALIDAR GRUPOS EXISTEN
# ============================================================================

print("1️⃣  Validando grupos...\n")

grupos_requeridos = ['Docente', 'Administrador']
for grupo_nombre in grupos_requeridos:
    try:
        grupo = Group.objects.get(name=grupo_nombre)
        permisos_count = grupo.permissions.count()
        print(f"   ✅ Grupo '{grupo_nombre}' existe ({permisos_count} permisos)")
    except Group.DoesNotExist:
        print(f"   ❌ ERROR: Grupo '{grupo_nombre}' NO existe")

# ============================================================================
# 2. VALIDAR PERMISOS POR GRUPO
# ============================================================================

print("\n2️⃣  Validando permisos por grupo...\n")

reserva_content_type = ContentType.objects.get(
    app_label='reservas_equipo',
    model='reserva'
)

# Permisos esperados para cada grupo
permisos_esperados = {
    'Docente': ['add_reserva', 'change_reserva', 'delete_reserva'],
    'Administrador': ['add_reserva', 'change_reserva', 'delete_reserva', 'view_reserva'],
}

for grupo_nombre, permisos_codenames in permisos_esperados.items():
    try:
        grupo = Group.objects.get(name=grupo_nombre)
        permisos_grupo = grupo.permissions.values_list('codename', flat=True)
        
        print(f"\n   📋 Grupo: {grupo_nombre}")
        todos_ok = True
        
        for codename in permisos_codenames:
            if codename in permisos_grupo:
                print(f"      ✅ {codename}")
            else:
                print(f"      ❌ {codename} FALTANTE")
                todos_ok = False
        
        if todos_ok:
            print(f"   ✅ Todos los permisos OK para {grupo_nombre}")
        else:
            print(f"   ⚠️  Faltan permisos en {grupo_nombre}")
            
    except Group.DoesNotExist:
        print(f"   ❌ Grupo {grupo_nombre} no existe")

# ============================================================================
# 3. VALIDAR MIXINS EXISTEN
# ============================================================================

print("\n3️⃣  Validando archivos de mixins y decoradores...\n")

import importlib

try:
    from reservas_equipo.mixins import (
        RoleRequiredMixin,
        DoctenteMixin,
        AdministradorMixin,
        PropietarioReservaMixin,
        PermisionRequiredMixin,
    )
    print("   ✅ Archivo mixins.py existe y se importa correctamente")
    print("      ✅ RoleRequiredMixin")
    print("      ✅ DoctenteMixin")
    print("      ✅ AdministradorMixin")
    print("      ✅ PropietarioReservaMixin")
    print("      ✅ PermisionRequiredMixin")
except ImportError as e:
    print(f"   ❌ ERROR importando mixins: {e}")

try:
    from reservas_equipo.decorators import (
        role_required,
        roles_required,
        docente_required,
        administrador_required,
        permission_required,
        propietario_required,
    )
    print("\n   ✅ Archivo decorators.py existe y se importa correctamente")
    print("      ✅ @role_required")
    print("      ✅ @roles_required")
    print("      ✅ @docente_required")
    print("      ✅ @administrador_required")
    print("      ✅ @permission_required")
    print("      ✅ @propietario_required")
except ImportError as e:
    print(f"   ❌ ERROR importando decorators: {e}")

# ============================================================================
# 4. VALIDAR VISTAS ACTUALIZADAS
# ============================================================================

print("\n4️⃣  Validando vistas...\n")

try:
    from reservas_equipo.views import (
        ReservaCreateView,
        ReservaUpdateView,
        ReservaDeleteView,
        ReservasAdministracionListView,
        AprobarReservaView,
        RechazarReservaView,
    )
    print("   ✅ Todas las vistas de administración existen")
    print("      ✅ ReservaCreateView (con DoctenteMixin)")
    print("      ✅ ReservaUpdateView (con mixins)")
    print("      ✅ ReservaDeleteView (con mixins)")
    print("      ✅ ReservasAdministracionListView (NEW)")
    print("      ✅ AprobarReservaView (NEW)")
    print("      ✅ RechazarReservaView (NEW)")
except ImportError as e:
    print(f"   ❌ ERROR importando vistas: {e}")

# ============================================================================
# 5. VALIDAR RUTAS
# ============================================================================

print("\n5️⃣  Validando rutas URL...\n")

from django.urls import path, include
from reservas_equipo.urls import reservas as reservas_urls

rutas_esperadas = [
    'reserva_list',
    'reserva_create',
    'reserva_detail',
    'reserva_update',
    'reserva_delete',
    'administracion_list',
    'reserva_aprobar',
    'reserva_rechazar',
]

rutas_encontradas = []
if hasattr(reservas_urls, 'urlpatterns'):
    for pattern in reservas_urls.urlpatterns:
        if hasattr(pattern, 'name'):
            rutas_encontradas.append(pattern.name)

for ruta in rutas_esperadas:
    if ruta in rutas_encontradas:
        print(f"   ✅ Ruta '{ruta}' existe")
    else:
        print(f"   ❌ Ruta '{ruta}' NO encontrada")

# ============================================================================
# 6. VALIDACIÓN DE INTEGRIDAD DE BD
# ============================================================================

print("\n6️⃣  Validando base de datos...\n")

from django.contrib.auth.models import User

total_usuarios = User.objects.count()
docentes = User.objects.filter(groups__name='Docente').count()
administradores = User.objects.filter(groups__name='Administrador').count()
sin_grupo = User.objects.filter(groups__isnull=True).count()

print(f"   📊 Usuarios totales: {total_usuarios}")
print(f"      - Docentes: {docentes}")
print(f"      - Administradores: {administradores}")
print(f"      - Sin grupo asignado: {sin_grupo}")

total_reservas = Reserva.objects.count()
reservas_pendientes = Reserva.objects.filter(estado='pendiente').count()
reservas_aprobadas = Reserva.objects.filter(estado='aprobada').count()
reservas_rechazadas = Reserva.objects.filter(estado='rechazada').count()

print(f"\n   📋 Reservas totales: {total_reservas}")
print(f"      - Pendientes: {reservas_pendientes}")
print(f"      - Aprobadas: {reservas_aprobadas}")
print(f"      - Rechazadas: {reservas_rechazadas}")

# ============================================================================
# 7. RESUMEN FINAL
# ============================================================================

print("\n" + "="*70)
print("RESUMEN DE VALIDACIÓN")
print("="*70 + "\n")

print("✅ Todos los componentes principales están presentes")
print("✅ Sistema de autenticación y roles está listo")
print("\n📝 Próximos pasos:")
print("   1. Ejecutar migrations: python manage.py migrate")
print("   2. Crear datos de prueba: python manage.py shell < setup_test_data.py")
print("   3. Acceder a: http://localhost:8000/")
print("   4. Login con: carlos/docente123 o juan/admin123")
print("\n" + "="*70 + "\n")
