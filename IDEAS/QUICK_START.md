# ⚡ Quick Start - Iniciar el Proyecto en 5 Minutos

## 🚀 Pasos Rápidos

### 1️⃣ Activar Entorno Virtual
```bash
# PowerShell
.\venv\Scripts\Activate.ps1

# CMD
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

### 2️⃣ Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3️⃣ Base de Datos
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear admin
python manage.py createsuperuser
# Usuario: admin
# Email: admin@test.com
# Password: admin123
```

### 4️⃣ Crear Datos de Prueba
```bash
python manage.py shell

# Copiar y pegar:
from reservas_equipo.models import Laboratorio
from django.contrib.auth.models import User

# Crear laboratorios
Laboratorio.objects.create(nombre='Lab Computación', capacidad=30)
Laboratorio.objects.create(nombre='Lab Física', capacidad=25)
Laboratorio.objects.create(nombre='Lab Química', capacidad=20)

# Crear usuario docente
User.objects.create_user('docente', 'docente@test.com', 'pass123', 
                         first_name='Juan', last_name='Pérez')

exit()
```

### 5️⃣ Ejecutar Servidor
```bash
python manage.py runserver
```

### 6️⃣ Acceder
- **Home**: http://localhost:8000/
- **Login**: http://localhost:8000/auth/login/
  - Usuario: `docente` / Contraseña: `pass123`
- **Admin**: http://localhost:8000/admin/
  - Usuario: `admin` / Contraseña: `admin123`
- **Mis Reservas**: http://localhost:8000/reservas/

---

## 📱 Rutas Disponibles

| Ruta | Descripción | Acceso |
|------|-------------|--------|
| `/` | Home | Público |
| `/auth/login/` | Iniciar sesión | Público |
| `/auth/logout/` | Cerrar sesión | Autenticado |
| `/reservas/` | Mis reservas | Autenticado |
| `/reservas/nueva/` | Crear reserva | Autenticado |
| `/reservas/<id>/` | Ver detalle | Propietario |
| `/reservas/<id>/editar/` | Editar | Propietario + pendiente |
| `/reservas/<id>/eliminar/` | Eliminar | Propietario + pendiente |
| `/admin/` | Panel admin | Staff |

---

## 🔍 Verificar que Funcione

### Checklist de Prueba

- [ ] Abrir http://localhost:8000/ → Ver landing page
- [ ] Click en "Iniciar Sesión" → Ir a login
- [ ] Ingresar usuario: `docente` / contraseña: `pass123` → Login exitoso
- [ ] Ir a "Nueva Reserva" → Formulario visible
- [ ] Llenar formulario → Crear reserva
- [ ] Ir a "Mis Reservas" → Ver reserva creada
- [ ] Ver detalle → Información correcta
- [ ] Editar → Cambios guardados
- [ ] Eliminar → Pregunta confirmación
- [ ] Logout → Volver al home
- [ ] Admin http://localhost:8000/admin/ → Login con admin
- [ ] Ver Laboratorios y Reservas en admin

---

## 📊 Base de Datos (Schema)

```sql
-- Usuarios
auth_user
├── id
├── username
├── password
├── email
├── first_name
├── last_name
└── is_staff

-- Laboratorios
reservas_equipo_laboratorio
├── id
├── nombre
├── descripcion
├── capacidad
├── activo
└── fecha_creacion

-- Reservas
reservas_equipo_reserva
├── id
├── usuario_id (FK)
├── laboratorio_id (FK)
├── fecha
├── hora_inicio
├── hora_fin
├── estado
├── motivo
├── fecha_creacion
└── fecha_actualizacion
```

---

## 🆘 Problemas Comunes

| Problema | Solución |
|----------|----------|
| "Module 'reservas_equipo' has no attribute 'apps'" | Ejecutar `python manage.py migrate` |
| "Table doesn't exist" | Ejecutar `python manage.py migrate` |
| Puerto 8000 ocupado | Usar `python manage.py runserver 8001` |
| Template not found | Verificar que templates esté en INSTALLED_APPS |
| 404 en /static/ | Verificar STATIC_URL y STATICFILES_DIRS |
| Login no funciona | Verificar que `LoginView` esté en URLs |

---

## 📚 Archivos Importantes

| Archivo | Propósito |
|---------|-----------|
| `README.md` | Documentación principal |
| `TRABAJO_EN_EQUIPO.md` | Guía de trabajo colaborativo |
| `COMANDOS_UTILES.md` | Referencia de comandos |
| `requirements.txt` | Dependencias Python |
| `manage.py` | CLI de Django |
| `.gitignore` | Archivos a ignorar en Git |

---

## 🎯 Próximos Pasos

1. **Leer README.md** - Entender la estructura completa
2. **Crear rama feature** - Comenzar a desarrollar
3. **Hacer cambios** - Trabajar en tu módulo
4. **Commit y Push** - Guardar cambios
5. **Pull Request** - Solicitar merge a develop

---

**¿Dudas? Revisa la documentación en README.md o TRABAJO_EN_EQUIPO.md**
