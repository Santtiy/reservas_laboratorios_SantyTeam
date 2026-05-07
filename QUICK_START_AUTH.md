# 🚀 GUÍA RÁPIDA DE REFERENCIA - Sistema de Auth

**Branch**: feature/ronald-auth | **Desarrollador**: Ronald | **Estado**: ✅ COMPLETADO

---

## ⚡ 3 PASOS PARA EMPEZAR

### 1️⃣ Aplicar Migración
```bash
python manage.py migrate
```
✅ Crea automáticamente: Grupo "Docente" + Grupo "Administrador"

### 2️⃣ Crear Datos de Prueba
```bash
python manage.py shell < setup_test_data.py
```
✅ Crea usuarios, laboratorios y reservas de ejemplo

### 3️⃣ Iniciar Servidor
```bash
python manage.py runserver
```
✅ Acceder a http://localhost:8000/

---

## 👤 CREDENCIALES DE PRUEBA

### Docente
- Usuario: `carlos`
- Contraseña: `docente123`
- Email: carlos@universidad.edu
- Acceso a: Crear/editar/eliminar propias reservas

### Administrador
- Usuario: `juan`
- Contraseña: `admin123`
- Email: juan@universidad.edu
- Acceso a: Panel admin, aprobar/rechazar todas

### Superuser
- Usuario: `admin`
- Contraseña: `admin123`
- Acceso: Total (Django admin)

---

## 🎯 ROLES Y PERMISOS

### GRUPO: DOCENTE
```
Permisos:
  ✅ add_reserva      (Crear)
  ✅ change_reserva   (Editar propias/pendientes)
  ✅ delete_reserva   (Eliminar propias/pendientes)

Acceso a URLs:
  ✅ /reservas/                     (Mis reservas)
  ✅ /reservas/nueva/               (Crear)
  ✅ /reservas/<id>/                (Ver)
  ✅ /reservas/<id>/editar/         (Editar)
  ✅ /reservas/<id>/eliminar/       (Eliminar)
  ❌ /reservas/administracion/      (Bloqueado)
```

### GRUPO: ADMINISTRADOR
```
Permisos:
  ✅ add_reserva      (Crear)
  ✅ change_reserva   (Editar cualquiera)
  ✅ delete_reserva   (Eliminar cualquiera)
  ✅ view_reserva     (Ver todas)

Acceso a URLs:
  ✅ /reservas/                     (Todas)
  ✅ /reservas/administracion/      (Panel admin)
  ✅ /reservas/<id>/aprobar/        (Aprobar)
  ✅ /reservas/<id>/rechazar/       (Rechazar)
  ✅ TODAS las URLs de Docente      (Acceso total)
```

---

## 🔧 CÓMO USAR MIXINS EN NUEVAS VISTAS

### Básico: Solo Docentes
```python
from reservas_equipo.mixins import DoctenteMixin

class MiVista(DoctenteMixin, ListView):
    model = Reserva
    # Solo Docentes → Acceso permitido
    # Otros → Error + Redirige
```

### Avanzado: Múltiples Roles
```python
from reservas_equipo.mixins import RoleRequiredMixin

class MiVista(RoleRequiredMixin, ListView):
    model = Reserva
    required_groups = ['Docente', 'Administrador']
    # Cualquiera de estos roles → Acceso permitido
```

### Propiedad: Solo si es Dueño
```python
from reservas_equipo.mixins import PropietarioReservaMixin

class MiVista(PropietarioReservaMixin, UpdateView):
    model = Reserva
    # Solo propietario O admin → Acceso permitido
    # Otros → Error + Redirige
```

### Permisos Django
```python
from reservas_equipo.mixins import PermisionRequiredMixin

class MiVista(PermisionRequiredMixin, DeleteView):
    model = Reserva
    required_permission = 'reservas_equipo.delete_reserva'
```

---

## 📝 CÓMO USAR DECORADORES (Vistas Función)

```python
from reservas_equipo.decorators import docente_required, administrador_required

@docente_required
def vista_docente(request):
    return render(request, 'template.html')

@administrador_required
def vista_admin(request):
    return render(request, 'template.html')
```

---

## 🧪 TESTING RÁPIDO

### Test 1: ¿Docente ve "Nueva Reserva"?
```
1. Login con carlos/docente123
2. Ver navbar
3. ✅ Debe ver "Nueva Reserva"
```

### Test 2: ¿Admin ve "Administración"?
```
1. Login con juan/admin123
2. Ver navbar
3. ✅ Debe ver "Administración" (naranja)
4. Click → Panel con todas las reservas
```

### Test 3: ¿No puede editar después de aprobar?
```
1. Ir a /reservas/<id>/editar/
2. Si estado = 'aprobada' → ❌ Error
3. Si estado = 'pendiente' → ✅ Permitido
```

### Test 4: ¿Panel admin solo para admins?
```
1. Login con carlos/docente123
2. Ir a /reservas/administracion/
3. ❌ Redirige a home con error
4. Login con juan/admin123
5. ✅ Muestra panel
```

---

## 📊 ESTRUCTURA DE ARCHIVOS

```
✅ CREADOS:
  └── reservas_equipo/
      ├── mixins.py                 # 5 mixins
      ├── decorators.py             # 6 decoradores
      └── migrations/
          └── 0002_create_groups_and_permissions.py
  
  └── templates/
      └── reservas/
          └── reserva_administracion_list.html
  
  └── AUTH_SYSTEM_DOCUMENTATION.md
  └── IMPLEMENTACION_RESUMEN.md
  └── setup_test_data.py
  └── validate_auth_system.py

✅ MODIFICADOS:
  └── reservas_equipo/
      ├── views.py                  # +3 vistas nuevas
      └── urls/
          └── reservas.py           # +3 rutas nuevas
  
  └── templates/
      └── base/
          └── navbar.html           # Dinámico por rol
```

---

## ⚙️ CONFIGURACIÓN

### settings.py - Ya Configurado ✅
```python
LOGIN_URL = 'auth:login'              # ✅
LOGIN_REDIRECT_URL = 'home'           # ✅
LOGOUT_REDIRECT_URL = 'home'          # ✅
```
No requiere cambios adicionales.

---

## 🆘 PROBLEMAS COMUNES

| Problema | Solución |
|---|---|
| "No tienes permiso" | Usuario no está en grupo → Asignar en admin |
| "Nueva Reserva" no aparece | Usuario sin grupo → Asignar a Docente |
| Migración falla | Ejecutar `python manage.py migrate --fake-initial` |
| Admin no puede editar | Es por diseño → Use aprobar/rechazar |

---

## 📚 DOCUMENTACIÓN COMPLETA

Para documentación detallada:

```bash
# Abrir documentación completa
cat AUTH_SYSTEM_DOCUMENTATION.md

# Ver resumen de implementación
cat IMPLEMENTACION_RESUMEN.md

# Validar sistema
python manage.py shell < validate_auth_system.py
```

---

## 🔗 RUTAS PRINCIPALES

```
GET  /                              → Home (dashboard)
GET  /admin/                        → Django admin
POST /auth/login/                   → Login
GET  /auth/logout/                  → Logout

GET  /reservas/                     → Mis reservas (docentes)
POST /reservas/nueva/               → Crear (docentes)
GET  /reservas/<id>/                → Detalle
POST /reservas/<id>/editar/         → Editar
POST /reservas/<id>/eliminar/       → Eliminar

GET  /reservas/administracion/      → Panel admin
POST /reservas/<id>/aprobar/        → Aprobar (admin)
POST /reservas/<id>/rechazar/       → Rechazar (admin)
```

---

## ✅ VERIFICACIÓN FINAL

```bash
# Validar que todo funciona
python manage.py shell < validate_auth_system.py

# Debe mostrar:
#   ✅ Grupos existen
#   ✅ Permisos asignados
#   ✅ Mixins importan
#   ✅ Vistas existen
#   ✅ Rutas configuradas
```

---

## 🎓 APRENDE MÁS

**Docstrings en Código**:
- Cada clase tiene explicación
- Cada método documentado
- Ejemplos de uso

**Video de Demostración** (futuro):
- Cómo loguearse
- Crear reserva como Docente
- Aprobar como Admin
- Ver panel admin

---

## 💾 HACER COMMIT

Cuando esté listo para merge a develop:

```bash
git add .
git commit -m "feat: implement complete authentication system

- Add role-based access control (RBAC)
- Create Docente and Administrador groups
- Implement 5 reusable mixins for authorization
- Add 3 admin views (list, approve, reject)
- Add data migration for groups and permissions
- Update templates with dynamic role-based navigation
- No breaking changes to existing CRUD operations"

git push origin feature/ronald-auth
```

---

**¿Más dudas? Revisa AUTH_SYSTEM_DOCUMENTATION.md o contacta a Ronald.**

✅ **SISTEMA COMPLETADO Y LISTO PARA USAR**
