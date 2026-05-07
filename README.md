# 📚 Sistema de Gestión de Reservas de Laboratorios

## 📌 Información General

**Proyecto**: Sistema de Gestión de Reservas de Laboratorios  
**Equipo**: SantyTeam (4 integrantes)  
**Tipo**: Parcial Universitario  
**Tecnologías**: Django 6.0, Python 3.10+, SQLite, Bootstrap 5, HTML5, CSS3

---

## 🏗️ Estructura del Proyecto

```
reservas_laboratorios_SantyTeam/
├── reservas_lab_equipo/          # Configuración del proyecto
│   ├── settings.py               # Configuración de Django
│   ├── urls.py                   # URLs principales
│   ├── wsgi.py
│   └── asgi.py
│
├── reservas_equipo/              # Aplicación principal
│   ├── models.py                 # Modelos de BD
│   ├── views.py                  # Vistas (CBV)
│   ├── forms.py                  # Formularios
│   ├── admin.py                  # Panel de administración
│   ├── urls/                     # URLs organizadas por módulo
│   │   ├── auth.py               # URLs de autenticación
│   │   ├── reservas.py           # URLs de reservas
│   │   └── __init__.py
│   └── migrations/               # Migraciones de BD
│
├── templates/                    # Templates HTML
│   ├── base/
│   │   ├── base.html             # Template base
│   │   └── navbar.html           # Navbar reutilizable
│   ├── auth/
│   │   └── login.html            # Login
│   ├── reservas/
│   │   ├── reserva_list.html     # Listado
│   │   ├── reserva_form.html     # Formulario
│   │   ├── reserva_detail.html   # Detalle
│   │   └── reserva_confirm_delete.html
│   └── home.html                 # Home
│
├── static/                       # Archivos estáticos
│   ├── css/
│   │   └── style.css             # Estilos personalizados
│   ├── js/
│   └── images/
│
├── manage.py                     # Comando de Django
├── requirements.txt              # Dependencias
└── db.sqlite3                    # Base de datos (después de migrate)
```

---

## 🎯 Requerimientos del Sistema

### 1️⃣ **Autenticación y Roles**
- ✅ Login/Logout
- ✅ Roles: Docente, Administrador
- ✅ LoginRequiredMixin en vistas protegidas

### 2️⃣ **Gestión de Reservas**
- ✅ CRUD completo
- ✅ Validación de conflictos horarios (base)
- ✅ Estados: pendiente, aprobada, rechazada

### 3️⃣ **Visualización**
- ✅ Filtros básicos
- ✅ Estadísticas en home
- ⏳ Exportación CSV (tarea futura)

---

## 📊 Modelos de Datos

### **Laboratorio**
```python
- nombre (CharField, único)
- descripcion (TextField)
- capacidad (IntegerField)
- activo (BooleanField)
- fecha_creacion (DateTimeField)
```

### **Reserva**
```python
- usuario (ForeignKey → User)
- laboratorio (ForeignKey → Laboratorio)
- fecha (DateField)
- hora_inicio (TimeField)
- hora_fin (TimeField)
- estado (CharField: pendiente, aprobada, rechazada)
- motivo (TextField)
- fecha_creacion (DateTimeField)
- fecha_actualizacion (DateTimeField)
```

---

## 🔐 Vistas Disponibles

### **HomeView**
- Ruta: `/`
- Acceso: Público (con contenido diferenciado)
- Estadísticas básicas si está logueado

### **LoginView**
- Ruta: `/auth/login/`
- Acceso: Público
- Formulario personalizado con Bootstrap

### **LogoutView**
- Ruta: `/auth/logout/`
- Redirecciona al home

### **ReservaListView** (CBV)
- Ruta: `/reservas/`
- Acceso: LoginRequiredMixin
- Paginación: 10 resultados por página
- Filtros: laboratorio, estado

### **ReservaCreateView** (CBV)
- Ruta: `/reservas/nueva/`
- Acceso: LoginRequiredMixin
- El usuario se asigna automáticamente

### **ReservaUpdateView** (CBV)
- Ruta: `/reservas/<id>/editar/`
- Acceso: Usuario propietario + estado pendiente

### **ReservaDeleteView** (CBV)
- Ruta: `/reservas/<id>/eliminar/`
- Acceso: Usuario propietario + estado pendiente

### **ReservaDetailView** (CBV)
- Ruta: `/reservas/<id>/`
- Acceso: Propietario o staff

---

## 🚀 Cómo Iniciar

### 1. **Activar el entorno virtual**
```bash
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

### 2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

### 3. **Crear migraciones**
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. **Crear superusuario (admin)**
```bash
python manage.py createsuperuser
```

### 5. **Cargar datos iniciales** (laboratorios)
```python
# En Django shell
python manage.py shell

>>> from reservas_equipo.models import Laboratorio
>>> Laboratorio.objects.create(nombre="Laboratorio de Computación", capacidad=30)
>>> Laboratorio.objects.create(nombre="Laboratorio de Física", capacidad=25)
>>> Laboratorio.objects.create(nombre="Laboratorio de Química", capacidad=20)
```

### 6. **Ejecutar el servidor**
```bash
python manage.py runserver
```

### 7. **Acceder**
- Home: `http://localhost:8000/`
- Admin: `http://localhost:8000/admin/`

---

## 📝 Configuración de Django

### **settings.py - Cambios Realizados**

✅ `INSTALLED_APPS` - Agregada app `reservas_equipo`  
✅ `TEMPLATES['DIRS']` - Configuradas carpetas de templates  
✅ `STATIC_URL` y `STATICFILES_DIRS` - Configurados archivos estáticos  
✅ `LOGIN_URL = 'login'` - URL de redireccionamiento  
✅ `LOGIN_REDIRECT_URL = 'home'` - Después de login  
✅ `LOGOUT_REDIRECT_URL = 'home'` - Después de logout  
✅ `LANGUAGE_CODE = 'es-es'` - Español  
✅ `TIME_ZONE = 'America/Bogota'` - Zona horaria  

---

## 🌿 Estrategia de Ramas para Trabajo en Equipo

### **Rama Principal**
```bash
main                 # Rama de producción (código estable)
├── develop          # Rama de desarrollo (integración)
```

### **Ramas por Integrante** (Evitar conflictos)

```bash
develop
├── feature/auth                    # Integrante 1: Autenticación y roles
│   ├── forms de login/logout
│   ├── Validaciones de roles
│   └── Permisos en vistas
│
├── feature/reservas-crud           # Integrante 2: CRUD de Reservas
│   ├── ReservaCreateView
│   ├── ReservaUpdateView
│   ├── ReservaDeleteView
│   └── Validaciones de horarios
│
├── feature/listado-filtros         # Integrante 3: Listado y Filtros
│   ├── ReservaListView mejorada
│   ├── Filtros avanzados
│   ├── Paginación
│   └── Búsqueda
│
└── feature/admin-estadisticas      # Integrante 4: Admin y Estadísticas
    ├── Mejoras en admin.py
    ├── Dashboard con gráficos
    ├── Exportación CSV
    └── Reportes
```

### **Comandos Git Recomendados**

```bash
# 1. Clonar/Actualizar
git clone <repositorio>
git pull origin develop

# 2. Crear rama feature
git checkout -b feature/auth
# O simplemente si develop existe:
git checkout -b feature/auth origin/develop

# 3. Realizar cambios y commits
git add .
git commit -m "feat(auth): agregar validación de login"

# 4. Cuando termines, push
git push origin feature/auth

# 5. Crear Pull Request (en GitHub)
# - Ir a GitHub
# - New Pull Request
# - Base: develop, Compare: feature/auth
# - Describir cambios
# - Esperar code review

# 6. Después de aprobar el PR
git checkout develop
git pull origin develop
git branch -d feature/auth
```

---

## ⚠️ Cómo Evitar Conflictos

### **REGLA 1: Cada integrante en su rama feature**
```bash
# ✅ CORRECTO
git checkout -b feature/auth
git checkout -b feature/reservas-crud
git checkout -b feature/listado

# ❌ EVITAR
# No trabajen todos en develop
```

### **REGLA 2: Archivos que CADA UNO modifica**

**Integrante 1 (Autenticación):**
- ✏️ `views.py` - LoginView, LogoutView
- ✏️ `forms.py` - LoginCustomForm
- ✏️ `templates/auth/` - Todos
- 🚫 NO tocar views de reservas

**Integrante 2 (CRUD Reservas):**
- ✏️ `views.py` - Create, Update, Delete Views
- ✏️ `models.py` - Validaciones de Reserva
- ✏️ `templates/reservas/reserva_form.html`
- ✏️ `templates/reservas/reserva_confirm_delete.html`

**Integrante 3 (Listado y Filtros):**
- ✏️ `views.py` - ReservaListView, DetailView
- ✏️ `forms.py` - FiltroReservasForm
- ✏️ `templates/reservas/reserva_list.html`
- ✏️ `templates/reservas/reserva_detail.html`

**Integrante 4 (Admin y Estadísticas):**
- ✏️ `admin.py` - Completo
- ✏️ `views.py` - HomeView (estadísticas)
- ✏️ `templates/home.html` - Gráficos
- 🚫 NO tocar vistas de usuario

### **REGLA 3: Archivos compartidos (cuidado)**

Si necesitas modificar:
- `models.py` → Coordina con el equipo antes
- `urls.py` → Usa namespaces, no habrá conflictos
- `settings.py` → Habla primero
- `base.html` → Solo estilos y navbar comunes

---

## 🎨 Próximas Mejoras (Tareas Futuras)

- 📊 Dashboard con gráficos de reservas
- 📧 Notificaciones por email
- 📥 Exportación a CSV/PDF
- 🔔 Sistema de aprobaciones avanzado
- 📱 Validación de conflictos automática
- 👥 Gestión de roles y permisos
- 📈 Reportes de ocupación

---

## 📚 Referencias Útiles

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap 5](https://getbootstrap.com/)
- [Git Workflow](https://git-scm.com/book/es/v2)
- [Python Best Practices](https://pep8.org/)

---

## 📞 Soporte

Para dudas sobre la estructura:
1. Revisar esta documentación
2. Consultar comentarios en el código
3. Revisar docstrings en models.py y views.py

---

**Última actualización**: Mayo 2026  
**Versión**: 1.0 (Base Inicial)
