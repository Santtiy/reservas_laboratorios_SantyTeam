"""
Script para crear datos de prueba (fixtures) para el sistema de autenticación.

Responsable: Ronald (Feature: ronald-auth)
Uso: python manage.py shell < setup_test_data.py
"""

from django.contrib.auth.models import User, Group
from reservas_equipo.models import Reserva
from datetime import datetime, timedelta

print("\n" + "="*70)
print("CREAR DATOS DE PRUEBA - SISTEMA DE RESERVAS")
print("="*70 + "\n")

# ============================================================================
# 1. VERIFICAR/CREAR GRUPOS
# ============================================================================

print("1️⃣  Creando grupos...")

docente_group, created = Group.objects.get_or_create(name='Docente')
if created:
    print("   ✅ Grupo 'Docente' creado")
else:
    print("   ℹ️  Grupo 'Docente' ya existe")

admin_group, created = Group.objects.get_or_create(name='Administrador')
if created:
    print("   ✅ Grupo 'Administrador' creado")
else:
    print("   ℹ️  Grupo 'Administrador' ya existe")

# ============================================================================
# 2. CREAR USUARIOS DE PRUEBA
# ============================================================================

print("\n2️⃣  Creando usuarios de prueba...\n")

# Docente 1
usuario_docente1, created = User.objects.get_or_create(
    username='carlos',
    defaults={
        'email': 'carlos@universidad.edu',
        'first_name': 'Carlos',
        'last_name': 'García',
        'is_active': True,
    }
)
if created:
    usuario_docente1.set_password('docente123')
    usuario_docente1.save()
    usuario_docente1.groups.add(docente_group)
    print(f"   ✅ Usuario DOCENTE creado: carlos (contraseña: docente123)")
else:
    print(f"   ℹ️  Usuario carlos ya existe")

# Docente 2
usuario_docente2, created = User.objects.get_or_create(
    username='maria',
    defaults={
        'email': 'maria@universidad.edu',
        'first_name': 'María',
        'last_name': 'López',
        'is_active': True,
    }
)
if created:
    usuario_docente2.set_password('docente123')
    usuario_docente2.save()
    usuario_docente2.groups.add(docente_group)
    print(f"   ✅ Usuario DOCENTE creado: maria (contraseña: docente123)")
else:
    print(f"   ℹ️  Usuario maria ya existe")

# Administrador
usuario_admin, created = User.objects.get_or_create(
    username='juan',
    defaults={
        'email': 'juan@universidad.edu',
        'first_name': 'Juan',
        'last_name': 'Martínez',
        'is_active': True,
    }
)
if created:
    usuario_admin.set_password('admin123')
    usuario_admin.save()
    usuario_admin.groups.add(admin_group)
    print(f"   ✅ Usuario ADMINISTRADOR creado: juan (contraseña: admin123)")
else:
    print(f"   ℹ️  Usuario juan ya existe")

# Superuser (para pruebas rápidas)
superuser, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@universidad.edu',
        'first_name': 'Admin',
        'last_name': 'System',
        'is_superuser': True,
        'is_staff': True,
    }
)
if created:
    superuser.set_password('admin123')
    superuser.save()
    print(f"   ✅ SUPERUSER creado: admin (contraseña: admin123)")
else:
    print(f"   ℹ️  Superuser admin ya existe")

# ============================================================================
# 3. DEFINIR LABORATORIOS DE PRUEBA
# ============================================================================

print("\n3️⃣  Definiendo laboratorios...\n")

laboratorios = [
    'Laboratorio de Informática',
    'Laboratorio de Química',
    'Laboratorio de Física',
]

for lab in laboratorios:
    print(f"   ✅ Laboratorio definido: {lab}")

# ============================================================================
# 4. CREAR RESERVAS DE PRUEBA
# ============================================================================

print("\n4️⃣  Creando reservas de prueba...\n")

# Reserva 1: Carlos - Pendiente
if Reserva.objects.filter(usuario=usuario_docente1, estado='pendiente').count() < 2:
    reserva1 = Reserva.objects.create(
        usuario=usuario_docente1,
        laboratorio=laboratorios[0],
        fecha=datetime.now().date() + timedelta(days=2),
        hora_inicio=datetime.strptime('09:00', '%H:%M').time(),
        hora_fin=datetime.strptime('11:00', '%H:%M').time(),
        motivo='Clase de Python - Nivel Básico',
        estado='pendiente'
    )
    print(f"   ✅ Reserva pendiente creada para Carlos")
else:
    print(f"   ℹ️  Ya existen reservas pendientes de Carlos")

# Reserva 2: Carlos - Aprobada
if Reserva.objects.filter(usuario=usuario_docente1, estado='aprobada').count() < 1:
    reserva2 = Reserva.objects.create(
        usuario=usuario_docente1,
        laboratorio=laboratorios[1],
        fecha=datetime.now().date() + timedelta(days=5),
        hora_inicio=datetime.strptime('14:00', '%H:%M').time(),
        hora_fin=datetime.strptime('16:00', '%H:%M').time(),
        motivo='Práctica de Laboratorio - Reacciones Químicas',
        estado='aprobada'
    )
    print(f"   ✅ Reserva aprobada creada para Carlos")
else:
    print(f"   ℹ️  Ya existen reservas aprobadas de Carlos")

# Reserva 3: María - Pendiente
if Reserva.objects.filter(usuario=usuario_docente2, estado='pendiente').count() < 1:
    reserva3 = Reserva.objects.create(
        usuario=usuario_docente2,
        laboratorio=laboratorios[2],
        fecha=datetime.now().date() + timedelta(days=3),
        hora_inicio=datetime.strptime('10:00', '%H:%M').time(),
        hora_fin=datetime.strptime('12:00', '%H:%M').time(),
        motivo='Proyecto Final - Física Experimental',
        estado='pendiente'
    )
    print(f"   ✅ Reserva pendiente creada para María")
else:
    print(f"   ℹ️  Ya existen reservas pendientes de María")

# Reserva 4: María - Rechazada
if Reserva.objects.filter(usuario=usuario_docente2, estado='rechazada').count() < 1:
    reserva4 = Reserva.objects.create(
        usuario=usuario_docente2,
        laboratorio=laboratorios[0],
        fecha=datetime.now().date() + timedelta(days=1),
        hora_inicio=datetime.strptime('15:00', '%H:%M').time(),
        hora_fin=datetime.strptime('17:00', '%H:%M').time(),
        motivo='Workshop - Programación Avanzada',
        estado='rechazada'
    )
    print(f"   ✅ Reserva rechazada creada para María")
else:
    print(f"   ℹ️  Ya existen reservas rechazadas de María")

# ============================================================================
# 5. RESUMEN
# ============================================================================

print("\n" + "="*70)
print("RESUMEN DE DATOS CREADOS")
print("="*70 + "\n")

print(f"👥 Usuarios totales: {User.objects.count()}")
print(f"   - Docentes: {User.objects.filter(groups__name='Docente').count()}")
print(f"   - Administradores: {User.objects.filter(groups__name='Administrador').count()}")
print(f"   - Sin grupo: {User.objects.filter(groups__isnull=True).count()}")

print(f"\n🏛️  Laboratorios distintos: {Reserva.objects.values('laboratorio').distinct().count()}")
print(f"\n📋 Reservas totales: {Reserva.objects.count()}")
print(f"   - Pendientes: {Reserva.objects.filter(estado='pendiente').count()}")
print(f"   - Aprobadas: {Reserva.objects.filter(estado='aprobada').count()}")
print(f"   - Rechazadas: {Reserva.objects.filter(estado='rechazada').count()}")

print("\n" + "="*70)
print("CREDENCIALES DE PRUEBA")
print("="*70 + "\n")

print("📝 DOCENTE:")
print("   Username: carlos")
print("   Password: docente123")
print("   Email: carlos@universidad.edu")
print("\n📝 DOCENTE 2:")
print("   Username: maria")
print("   Password: docente123")
print("   Email: maria@universidad.edu")
print("\n📝 ADMINISTRADOR:")
print("   Username: juan")
print("   Password: admin123")
print("   Email: juan@universidad.edu")
print("\n📝 SUPERUSER:")
print("   Username: admin")
print("   Password: admin123")
print("   Email: admin@universidad.edu")
print("\n" + "="*70)
print("✅ SETUP COMPLETADO")
print("="*70 + "\n")
