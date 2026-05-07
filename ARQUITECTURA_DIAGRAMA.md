# 📐 DIAGRAMA DE ARQUITECTURA - Sistema de Autenticación

## 🔐 FLUJO GENERAL DE AUTENTICACIÓN Y AUTORIZACIÓN

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USUARIO ACCEDE A URL                        │
│                     (ej: /reservas/administracion/)                 │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                ┌─────────────▼──────────────┐
                │    ¿USUARIO LOGUEADO?      │
                └─────────────┬──────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                  NO│                   │YES
                    │                   │
          ┌─────────▼────────┐  ┌──────▼──────────────────────┐
          │ REDIRIGE A LOGIN │  │ ¿USUARIO TIENE GRUPO?        │
          │   (auth:login)   │  │ (Docente/Administrador)     │
          └──────────────────┘  └──────┬──────────┬────────────┘
                                       │          │
                                      NO         YES
                                       │          │
                                   ┌───▼──────────▼────┐
                                   │   ¿ROL PERMITIDO?  │
                                   │  (DoctenteMixin,   │
                                   │ AdministradorMixin)│
                                   └───┬──────────┬─────┘
                                       │          │
                                      NO         YES
                                       │          │
                            ┌──────────▼──┐  ┌───▼──────────┐
                            │   ERROR      │  │ ¿PROPIETARIO?│
                            │  Redirige    │  │ (Propiedad   │
                            │  a home      │  │  del recurso)│
                            └──────────────┘  └───┬──┬───────┘
                                                   │  │
                                                  NO  YES
                                                   │  │
                                        ┌──────────▼──┴─┐
                                        │   ERROR       │
                                        │  Redirige    │
                                        │   a home      │
                                        └──────────────┘
                                                ▼
                                        ┌────────────────┐
                                        │  ✅ ACCESO     │
                                        │   PERMITIDO    │
                                        │   Cargar Vista │
                                        └────────────────┘
```

---

## 🏗️ ARQUITECTURA DE CAPAS

```
┌──────────────────────────────────────────────────────────────────┐
│                          TEMPLATES (HTML)                         │
│  ┌──────────────────────────────────────────────────────────────┤
│  │ • navbar.html (Dinámico)  → Muestra opciones por rol        │
│  │ • reserva_list.html       → Listar (docente/admin)          │
│  │ • reserva_form.html       → Crear/editar                     │
│  │ • reserva_administracion_list.html → Panel admin            │
│  └──────────────────────────────────────────────────────────────┘
└────────────────────┬─────────────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────────────────┐
│                    VISTAS (CBV - Class-Based Views)              │
│  ┌──────────────────────────────────────────────────────────────┤
│  │ DOCENTES:                                                    │
│  │  • ReservaCreateView      (DoctenteMixin + LoginRequired)   │
│  │  • ReservaUpdateView      (DoctenteMixin + Propietario)     │
│  │  • ReservaDeleteView      (DoctenteMixin + Propietario)     │
│  │                                                              │
│  │ ADMINISTRADORES:                                            │
│  │  • ReservasAdministracionListView (AdministradorMixin)     │
│  │  • AprobarReservaView     (AdministradorMixin)             │
│  │  • RechazarReservaView    (AdministradorMixin)             │
│  └──────────────────────────────────────────────────────────────┘
└────────────────────┬─────────────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────────────────┐
│                     MIXINS (Control de Acceso)                   │
│  ┌──────────────────────────────────────────────────────────────┤
│  │ ┌────────────────────────────────────────────────────────┐  │
│  │ │ RoleRequiredMixin (Genérico)                           │  │
│  │ │  ├─ DoctenteMixin        (Docentes específico)        │  │
│  │ │  └─ AdministradorMixin   (Administradores específico) │  │
│  │ └────────────────────────────────────────────────────────┘  │
│  │ ┌────────────────────────────────────────────────────────┐  │
│  │ │ PropietarioReservaMixin (Validar propiedad del objeto)│  │
│  │ └────────────────────────────────────────────────────────┘  │
│  │ ┌────────────────────────────────────────────────────────┐  │
│  │ │ PermisionRequiredMixin (Permisos Django específicos)  │  │
│  │ └────────────────────────────────────────────────────────┘  │
│  └──────────────────────────────────────────────────────────────┘
└────────────────────┬─────────────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────────────────┐
│               DECORADORES (Para Vistas Función - Optional)       │
│  ┌──────────────────────────────────────────────────────────────┤
│  │ @docente_required           →  Solo Docentes                │
│  │ @administrador_required     →  Solo Administradores         │
│  │ @role_required('Rol')       →  Rol específico              │
│  │ @permission_required('perm')→  Permiso Django específico    │
│  │ @propietario_required(Model)→  Propiedad del recurso       │
│  └──────────────────────────────────────────────────────────────┘
└────────────────────┬─────────────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────────────────┐
│         MODELOS & BASE DE DATOS (Django ORM)                    │
│  ┌──────────────────────────────────────────────────────────────┤
│  │ USER (Django)                                                │
│  │  ├─ username, email, password                               │
│  │  └─ groups (M2M) → [Docente, Administrador]               │
│  │                                                              │
│  │ GROUP (Django)                                               │
│  │  ├─ Docente (con permisos específicos)                      │
│  │  └─ Administrador (con permisos específicos)               │
│  │                                                              │
│  │ PERMISSION (Django)                                         │
│  │  ├─ add_reserva                                            │
│  │  ├─ change_reserva                                         │
│  │  ├─ delete_reserva                                         │
│  │  └─ view_reserva                                           │
│  │                                                              │
│  │ RESERVA (Custom)                                            │
│  │  ├─ usuario (FK → User)                                    │
│  │  ├─ laboratorio (FK → Laboratorio)                         │
│  │  ├─ estado (pendiente/aprobada/rechazada)                 │
│  │  └─ validaciones de negocio                                │
│  └──────────────────────────────────────────────────────────────┘
└──────────────────────────────────────────────────────────────────┘
```

---

## 🔄 CICLO DE VIDA DE UNA SOLICITUD

```
1. USUARIO SOLICITA /reservas/nueva/
   │
   ├─→ Django Routing → reservas_urls.py
   │
   ├─→ Vista: ReservaCreateView
   │
   ├─→ Mixins Ejecutan:
   │   ├─ DoctenteMixin.dispatch()
   │   │  └─ Verifica: ¿Usuario es Docente? ✅/❌
   │   │
   │   └─ CreateView ejecuta form_valid()
   │      └─ Guarda en BD
   │
   └─→ Respuesta: Template o Redirige
```

---

## 📊 MATRIZ DE PERMISOS

```
                    │ LOGIN │ CREAR │ VER  │ EDITAR │ ELIMINAR │ APROBAR │ RECHAZAR │
────────────────────┼───────┼───────┼──────┼────────┼──────────┼─────────┼──────────┤
DOCENTE             │  ✅   │  ✅   │  ✅* │  ✅*   │   ✅*    │   ❌    │   ❌     │
ADMINISTRADOR       │  ✅   │  ✅   │  ✅✅ │ ✅✅   │  ✅✅   │  ✅     │   ✅     │
NO AUTENTICADO      │  ✅   │  ❌   │  ❌  │  ❌    │   ❌     │   ❌    │   ❌     │
────────────────────┼───────┼───────┼──────┼────────┼──────────┼─────────┼──────────┤
* = Solo propias reservas en estado pendiente
✅ = Permitido
✅✅ = Permitido (cualquiera)
❌ = Denegado
```

---

## 🎯 ROLES Y RESPONSABILIDADES

```
┌─────────────────────────────────────────────────────────────┐
│              GRUPO: DOCENTE                                 │
├─────────────────────────────────────────────────────────────┤
│ Responsabilidades:                                          │
│  1. Crear reservas de laboratorios                         │
│  2. Editar sus propias reservas (si están pendientes)     │
│  3. Eliminar sus propias reservas (si están pendientes)   │
│  4. Ver su historial de reservas                          │
│                                                             │
│ Limitaciones:                                              │
│  ✗ No puede ver reservas de otros Docentes               │
│  ✗ No puede editar/eliminar reservas aprobadas           │
│  ✗ No puede acceder a panel de administración            │
│  ✗ No puede aprobar ni rechazar reservas                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│          GRUPO: ADMINISTRADOR                               │
├─────────────────────────────────────────────────────────────┤
│ Responsabilidades:                                          │
│  1. Ver todas las reservas del sistema                     │
│  2. Aprobar reservas pendientes                            │
│  3. Rechazar reservas pendientes                           │
│  4. Filtrar reservas por estado y laboratorio             │
│  5. Tomar decisiones sobre asignación de recursos        │
│                                                             │
│ Privilegios Especiales:                                    │
│  ✓ Acceso total a panel de administración                │
│  ✓ Puede ver todas las reservas                          │
│  ✓ Puede editar/eliminar cualquier reserva               │
│  ✓ Hereda acceso de Docente                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔐 SEGURIDAD EN CAPAS

```
┌──────────────────────────────────────┐
│      NIVEL 1: AUTENTICACIÓN          │
│   ¿Está el usuario logueado?        │
│   Django Auth Middleware             │
└──────────┬───────────────────────────┘
           │
           ├─→ NO: Redirige a login
           │
           └─→ SÍ: Continúa
                   │
┌──────────────────▼──────────────────┐
│       NIVEL 2: AUTORIZACIÓN          │
│   ¿Pertenece al grupo requerido?    │
│   Mixin (RoleRequiredMixin)          │
└──────────┬───────────────────────────┘
           │
           ├─→ NO: Error 403 + Redirige
           │
           └─→ SÍ: Continúa
                   │
┌──────────────────▼──────────────────┐
│      NIVEL 3: VALIDACIÓN RECURSO     │
│   ¿Pertenece el objeto al usuario?  │
│   Mixin (PropietarioReservaMixin)    │
└──────────┬───────────────────────────┘
           │
           ├─→ NO: Error 403 + Redirige
           │
           └─→ SÍ: Continúa
                   │
┌──────────────────▼──────────────────┐
│    NIVEL 4: LÓGICA DE NEGOCIO        │
│   ¿Cumple validaciones especiales?  │
│   (ej: ¿reserva está pendiente?)    │
└──────────┬───────────────────────────┘
           │
           ├─→ NO: Error 400 + Mensaje
           │
           └─→ SÍ: ✅ ACCESO PERMITIDO
                   Ejecuta la acción
```

---

## 📈 ESCALABILIDAD - AGREGAR NUEVO ROL

```
Ejemplo: Agregar rol "SUPERVISOR"

PASO 1: Crear Grupo
┌──────────────────────────────────────┐
│ supervisor_group = Group.objects     │
│   .create(name='Supervisor')         │
└──────────────────────────────────────┘
                │
PASO 2: Asignar Permisos
┌──────────────────────────────────────┐
│ supervisor_group.permissions.add(    │
│   Permission.objects.filter(         │
│     codename='view_reserva'          │
│   )                                  │
│ )                                    │
└──────────────────────────────────────┘
                │
PASO 3: Crear Mixin
┌──────────────────────────────────────┐
│ class SupervisorMixin(               │
│   RoleRequiredMixin                  │
│ ):                                   │
│   required_groups = 'Supervisor'    │
└──────────────────────────────────────┘
                │
PASO 4: Usar en Vista
┌──────────────────────────────────────┐
│ class MiVista(SupervisorMixin,      │
│   ListView):                         │
│   model = Reserva                    │
└──────────────────────────────────────┘
                │
PASO 5: Asignar Usuarios
┌──────────────────────────────────────┐
│ user.groups.add(supervisor_group)   │
└──────────────────────────────────────┘

✅ Nuevo rol listo para usar
```

---

## 📊 FLUJO DE APROBACIÓN DE RESERVAS

```
DOCENTE CREA RESERVA
       │
       ▼
RESERVA GUARDADA (estado: pendiente)
       │
       ▼
APARECE EN PANEL DE ADMINISTRACIÓN
       │
       ├─────────────────────┬─────────────────────┐
       │                     │                     │
       ▼                     ▼                     ▼
   [APROBAR]           [RECHAZAR]            [SIN ACCIÓN]
       │                     │                     │
       ▼                     ▼                     ▼
   aprobada             rechazada              pendiente
       │                     │                     │
       ▼                     ▼                     ▼
DOCENTE VE              DOCENTE VE           DOCENTE VE
APROBADA EN             RECHAZADA EN          PENDIENTE EN
SUS RESERVAS            SUS RESERVAS          SUS RESERVAS
```

---

## 🧪 TESTING - CASOS DE USO

```
CASO 1: Docente intenta crear reserva
┌──────────────────────────────────────┐
│ 1. Login con carlos/docente123       │
│ 2. Ir a /reservas/nueva/            │
│ 3. ✅ Muestra formulario            │
│ 4. Llenar y guardar                 │
│ 5. ✅ Reserva guardada              │
└──────────────────────────────────────┘

CASO 2: Docente intenta acceder a admin
┌──────────────────────────────────────┐
│ 1. Login con carlos/docente123       │
│ 2. Ir a /reservas/administracion/   │
│ 3. ❌ Redirige a home                │
│ 4. Muestra: "No tienes permiso"     │
└──────────────────────────────────────┘

CASO 3: Admin aprueba reserva
┌──────────────────────────────────────┐
│ 1. Login con juan/admin123           │
│ 2. Ir a /reservas/administracion/   │
│ 3. ✅ Ve todas las reservas         │
│ 4. Click en botón [APROBAR]         │
│ 5. ✅ Estado cambia a "aprobada"    │
│ 6. Botones se desactivan            │
└──────────────────────────────────────┘

CASO 4: Docente intenta editar aprobada
┌──────────────────────────────────────┐
│ 1. Login con carlos/docente123       │
│ 2. Ir a /reservas/<id>/editar/      │
│ 3. Si estado = 'aprobada'           │
│    ❌ Error: "Solo pendientes"       │
│ 4. Si estado = 'pendiente'          │
│    ✅ Muestra formulario            │
└──────────────────────────────────────┘
```

---

**Diagrama actualizado**: 7 de mayo de 2026  
**Versión**: 1.0 - Sistema Completo
