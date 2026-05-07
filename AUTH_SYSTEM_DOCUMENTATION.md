# 🔐 Documentación del Sistema de Autenticación y Roles

**Responsable**: Ronald (Feature: feature/ronald-auth)  
**Fecha**: 7 de mayo de 2026  
**Estado**: ✅ Completado

---

## 📋 Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Estructura de Roles y Permisos](#estructura-de-roles-y-permisos)
3. [Archivos Modificados/Creados](#archivos-modificadoscreados)
4. [Cómo Usar](#cómo-usar)
5. [Testing del Sistema](#testing-del-sistema)
6. [Problemas Comunes](#problemas-comunes)

---

## 🎯 Descripción General

Este sistema implementa un control de acceso robusto basado en **roles y permisos de Django**:

- ✅ **Dos grupos de usuarios**: Docente y Administrador
- ✅ **Mixins personalizados**: Para validación de roles en vistas
- ✅ **Decoradores opcionales**: Para vistas basadas en funciones
- ✅ **Templates adaptables**: Muestra opciones según rol del usuario
- ✅ **Sin romper CRUD existente**: Todas las vistas anteriores siguen funcionando

---

## 👥 Estructura de Roles y Permisos

### Grupo: DOCENTE

**Permisos**:
- ✅ `reservas_equipo.add_reserva` - Crear reservas propias
- ✅ `reservas_equipo.change_reserva` - Editar reservas propias (estado pendiente)
- ✅ `reservas_equipo.delete_reserva` - Eliminar reservas propias (estado pendiente)

**Acceso a vistas**:
- `/reservas/` - Lista de propias reservas
- `/reservas/nueva/` - Crear nueva reserva
- `/reservas/<id>/` - Ver detalle de propia reserva
- `/reservas/<id>/editar/` - Editar propia reserva (pendiente)
- `/reservas/<id>/eliminar/` - Eliminar propia reserva (pendiente)

### Grupo: ADMINISTRADOR

**Permisos**:
- ✅ `reservas_equipo.add_reserva` - Crear reservas
- ✅ `reservas_equipo.change_reserva` - Editar/aprobar/rechazar cualquier reserva
- ✅ `reservas_equipo.delete_reserva` - Eliminar reservas
- ✅ `reservas_equipo.view_reserva` - Ver todas las reservas

**Acceso a vistas**:
- Todas las vistas de Docente
- `/reservas/administracion/` - Panel de administración (todas las reservas)
- `/reservas/<id>/aprobar/` - Aprobar reserva
- `/reservas/<id>/rechazar/` - Rechazar reserva

### Grupo: SUPERUSER

- ✅ Acceso a todo (no necesita grupo)

---

## 📁 Archivos Modificados/Creados

### ✅ CREADOS

```
reservas_equipo/
├── mixins.py (NUEVO)
│   ├── RoleRequiredMixin          # Validar pertenencia a grupos
│   ├── DoctenteMixin              # Restricción específica Docente
│   ├── AdministradorMixin         # Restricción específica Administrador
│   ├── PropietarioReservaMixin    # Validar propiedad del objeto
│   └── PermisionRequiredMixin     # Validar permisos específicos
│
├── decorators.py (NUEVO)
│   ├── @role_required()           # Decorador genérico
│   ├── @roles_required()          # Múltiples roles
│   ├── @docente_required()        # Decorador Docente
│   ├── @administrador_required()  # Decorador Administrador
│   └── @propietario_required()    # Decorador propiedad
│
├── migrations/
│   └── 0002_create_groups_and_permissions.py (NUEVO)
│       └── Crea grupos y asigna permisos automáticamente
│
templates/reservas/
└── reserva_administracion_list.html (NUEVO)
    └── Panel visual para administradores
```

### ✅ MODIFICADOS

```
reservas_equipo/
├── views.py
│   ├── ReservaCreateView     → Agregado DoctenteMixin
│   ├── ReservaUpdateView     → Agregado mixins + validación estado
│   ├── ReservaDeleteView     → Agregado mixins + validación estado
│   ├── ReservasAdministracionListView (NUEVA)
│   ├── AprobarReservaView    (NUEVA)
│   └── RechazarReservaView   (NUEVA)
│
├── urls/reservas.py
│   ├── Ruta administracion/
│   ├── Ruta <id>/aprobar/
│   └── Ruta <id>/rechazar/
│
templates/base/
└── navbar.html
    └── Agregadas opciones condicionales por rol
```

---

## 🚀 Cómo Usar

### 1. INSTALAR MIGRACIÓN

```bash
# Crear y aplicar migración
python manage.py migrate

# Verificar que se crearon los grupos
python manage.py shell
>>> from django.contrib.auth.models import Group
>>> Group.objects.all()
<QuerySet [<Group: Docente>, <Group: Administrador>]>
```

### 2. CREAR USUARIOS DE PRUEBA

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User, Group

# Crear usuario Docente
docente = User.objects.create_user(
    username='carlos',
    email='carlos@universidad.edu',
    password='docente123',
    first_name='Carlos',
    last_name='García'
)
grupo_docente = Group.objects.get(name='Docente')
docente.groups.add(grupo_docente)

# Crear usuario Administrador
admin = User.objects.create_user(
    username='juan',
    email='juan@universidad.edu',
    password='admin123',
    first_name='Juan',
    last_name='Martínez'
)
grupo_admin = Group.objects.get(name='Administrador')
admin.groups.add(grupo_admin)

print("✅ Usuarios creados exitosamente")
```

### 3. PROBAR EN LA APLICACIÓN

**Como Docente (carlos/docente123)**:
- Ir a http://localhost:8000/
- Login con usuario: `carlos`
- Ver "Mis Reservas" y "Nueva Reserva" en navbar
- ❌ NO ver "Administración"

**Como Administrador (juan/admin123)**:
- Ir a http://localhost:8000/
- Login con usuario: `juan`
- Ver "Administración" en navbar (en naranja)
- Ir a `/reservas/administracion/`
- Ver todas las reservas del sistema
- Poder aprobar/rechazar reservas pendientes

---

## 🧪 Testing del Sistema

### Test 1: Restricción de Acceso

```python
# Como Docente, intentar acceder a administracion/
# → ❌ Debe redirigir con mensaje "No tienes permisos"

# Como Administrador
# → ✅ Debe mostrar panel
```

### Test 2: Propiedad de Recursos

```python
# Carlos (Docente) crea reserva
# → ✅ Puede editar/eliminar su propia reserva

# Carlos intenta editar/eliminar reserva de otro usuario
# → ❌ Debe mostrar error de permiso

# Juan (Admin) intenta editar reserva de Carlos
# → ✅ Debe permitir (admin tiene acceso total)
```

### Test 3: Validación de Estado

```python
# Carlos tiene una reserva aprobada
# → ❌ NO puede editarla (solo pendientes)
# → ❌ NO puede eliminarla (solo pendientes)

# Juan (Admin) puede cambiar de aprobada a rechazada
# → ✅ Los botones de aprobar/rechazar se desactivan después de cambiar estado
```

### Test 4: CRUD Original Intacto

```python
# Todos los endpoints CRUD siguen funcionando normalmente
# → Login + Logout: ✅ Funciona
# → Crear reserva: ✅ Funciona (con restricción Docente)
# → Editar reserva: ✅ Funciona (con restricción Docente + Propietario)
# → Eliminar reserva: ✅ Funciona (con restricción Docente + Propietario)
# → Ver detalle: ✅ Funciona
```

---

## 🔧 Uso de Mixins en Nuevas Vistas

### Ejemplo: Vista que solo Docentes pueden acceder

```python
from django.views.generic import ListView
from reservas_equipo.mixins import DoctenteMixin
from .models import Reserva

class MiVistaDocente(DoctenteMixin, ListView):
    model = Reserva
    template_name = 'mi_template.html'
    
    # Automáticamente solo Docentes pueden acceder
    # Si no tiene permiso → redirige a 'home' con mensaje
```

### Ejemplo: Vista de propiedad

```python
from reservas_equipo.mixins import PropietarioReservaMixin

class MiVistaPropiedad(PropietarioReservaMixin, UpdateView):
    model = Reserva
    fields = ['laboratorio', 'fecha', 'hora_inicio', 'hora_fin']
    
    # Verifica:
    # 1. Usuario autenticado
    # 2. Usuario es propietario O administrador O superuser
    # Si falla → muestra error con estilo
```

### Ejemplo: Múltiples roles permitidos

```python
from reservas_equipo.mixins import RoleRequiredMixin

class MiVistaMultiRol(RoleRequiredMixin, ListView):
    model = Reserva
    required_groups = ['Docente', 'Administrador']  # Cualquiera de estos
    
    # Permite Docentes O Administradores
```

---

## 💾 Uso de Decoradores (FBV)

Si prefieres vistas basadas en funciones:

```python
from django.shortcuts import render
from reservas_equipo.decorators import docente_required, administrador_required

@docente_required
def mi_vista_docente(request):
    return render(request, 'template.html')

@administrador_required
def mi_vista_admin(request):
    return render(request, 'template.html')
```

---

## ⚠️ Problemas Comunes

### Problema 1: "No tienes permiso para acceder"

**Causa**: Usuario no está en ningún grupo
**Solución**: Asignar usuario a grupo en Django admin o shell:

```python
user.groups.add(Group.objects.get(name='Docente'))
```

### Problema 2: Botón "Nueva Reserva" no aparece

**Causa**: Usuario no está en grupo Docente
**Solución**: Verificar en navbar que se evalúa `user.groups.all|length > 0`

### Problema 3: Migración falla

**Causa**: Modelo Reserva no existe o ContentType no está registrado
**Solución**:

```bash
python manage.py makemigrations
python manage.py migrate --fake-initial  # Si es primera vez
```

### Problema 4: Admin intenta editar pero ve solo lectura

**Causa**: PropietarioReservaMixin solo devuelve objeto, no permite editar
**Solución**: Es por diseño. Admin debe rechazar/aprobar, no editar directamente

---

## 📊 Diagrama de Flujo

```
Usuario Accede a Ruta
    ↓
¿Está autenticado? (LoginRequiredMixin)
    ├→ NO: Redirige a login
    │
    └→ SÍ: ¿Tiene rol requerido?
        ├→ NO: Redirige a home + mensaje error
        │
        └→ SÍ: ¿Es propietario/valida negocio?
            ├→ NO: Redirige a home + mensaje error
            │
            └→ SÍ: ✅ ACCESO PERMITIDO
```

---

## 🔑 Resumen de Cambios

| Componente | Antes | Después |
|---|---|---|
| **Control Acceso** | LoginRequiredMixin básico | Mixins + Roles + Permisos |
| **Vistas Docente** | Sin validación rol | Con DoctenteMixin |
| **Panel Admin** | No existía | ReservasAdministracionListView |
| **Aprobar/Rechazar** | No existía | AprobarReservaView + RechazarReservaView |
| **Navbar** | Opciones fijas | Opciones dinámicas por rol |
| **Escalabilidad** | Limitada | Fácil agregar nuevos roles |

---

## ✅ Checklist de Implementación

- [x] Mixins personalizados creados
- [x] Decoradores opcionales creados
- [x] Migration para grupos y permisos
- [x] Vistas CRUD actualizadas
- [x] Vistas de administración creadas
- [x] URLs actualizadas
- [x] Templates actualizados
- [x] Navbar dinámico
- [x] Sin romper arquitectura existente
- [x] Documentación completa

---

## 📞 Contacto y Soporte

Para dudas o problemas: **Ronald** (Feature Branch: feature/ronald-auth)

---

**Última actualización**: 7 de mayo de 2026  
**Versión**: 1.0 - Initial Release
