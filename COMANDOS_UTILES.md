# 🚀 Comandos Útiles - Sistema de Reservas

## 🔧 Configuración Inicial

```bash
# 1. Crear entorno virtual (si aún no existe)
python -m venv venv

# 2. Activar entorno (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# 3. Activar entorno (Windows CMD)
venv\Scripts\activate.bat

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Hacer migraciones
python manage.py makemigrations
python manage.py migrate

# 6. Crear superusuario (admin)
python manage.py createsuperuser

# 7. Crear laboratorios iniciales
python manage.py shell < scripts/cargar_laboratorios.py
```

---

## 🏃 Comandos para Desarrollo

```bash
# Ejecutar servidor
python manage.py runserver

# Ejecutar en puerto específico
python manage.py runserver 8001

# Hacer cambios en modelos
python manage.py makemigrations
python manage.py migrate

# Ver estado de migraciones
python manage.py showmigrations

# Revertir una migración
python manage.py migrate app_name 0002  # Volver a migración 0002

# Ejecutar tests (cuando existan)
python manage.py test

# Ver SQL de una query
python manage.py sqlmigrate app_name 0001
```

---

## 🐚 Comandos Django Shell

```bash
# Abrir shell
python manage.py shell

# Dentro del shell:

# --- Crear Usuarios ---
from django.contrib.auth.models import User

# Crear usuario normal
user = User.objects.create_user('docente1', 'docente@test.com', 'pass123')
user.first_name = 'Juan'
user.last_name = 'Pérez'
user.save()

# Crear admin
admin = User.objects.create_superuser('admin', 'admin@test.com', 'admin123')

# --- Crear Laboratorios ---
from reservas_equipo.models import Laboratorio

Laboratorio.objects.create(nombre='Lab Computación', capacidad=30)
Laboratorio.objects.create(nombre='Lab Física', capacidad=25)
Laboratorio.objects.create(nombre='Lab Química', capacidad=20)

# --- Crear Reservas ---
from reservas_equipo.models import Reserva
from datetime import date, time, timedelta

lab = Laboratorio.objects.first()
res = Reserva.objects.create(
    usuario=user,
    laboratorio=lab,
    fecha=date.today() + timedelta(days=1),
    hora_inicio=time(9, 0),
    hora_fin=time(11, 0),
    motivo='Clase práctica',
    estado='pendiente'
)

# --- Queries útiles ---
all_users = User.objects.all()
reservas_pendientes = Reserva.objects.filter(estado='pendiente')
reservas_usuario = Reserva.objects.filter(usuario=user)

# Ver todas las reservas
for res in Reserva.objects.all():
    print(f"{res.usuario} - {res.laboratorio} - {res.fecha}")

# Exit
exit()
```

---

## 📝 Comandos Git

```bash
# --- Setup Inicial ---
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"

# --- Branches ---
git branch                          # Ver ramas locales
git branch -a                       # Ver todas las ramas
git branch feature/mi-rama          # Crear rama
git checkout feature/mi-rama        # Cambiar a rama
git checkout -b feature/mi-rama     # Crear y cambiar

# --- Estado ---
git status                          # Ver estado
git diff                            # Ver cambios
git log --oneline                   # Ver commits

# --- Commits ---
git add .                           # Agregar todos los cambios
git add archivo.py                  # Agregar archivo específico
git commit -m "feat: agregar login" # Hacer commit
git push origin feature/mi-rama     # Subir rama

# --- Pull Request ---
# Ir a GitHub y crear Pull Request desde la interfaz

# --- Merge ---
git checkout develop
git pull origin develop
git merge feature/mi-rama           # Mergear en local
git push origin develop             # Subir a GitHub

# --- Limpiar ---
git branch -d feature/mi-rama       # Eliminar rama local
git push origin --delete feature/mi-rama  # Eliminar en GitHub
```

---

## 🧹 Mantenimiento

```bash
# Limpiar archivos temporales
python manage.py cleanup

# Recolectar archivos estáticos (producción)
python manage.py collectstatic

# Crear respaldo de BD
sqlite3 db.sqlite3 ".dump" > backup.sql

# Ver usuarios
python manage.py shell -c "
from django.contrib.auth.models import User
for u in User.objects.all():
    print(f'{u.username} - {u.email}')"

# Cambiar contraseña
python manage.py changepassword username

# Eliminar usuario
python manage.py shell -c "
from django.contrib.auth.models import User
User.objects.get(username='username').delete()
"
```

---

## 🐛 Troubleshooting

```bash
# Problema: No hay módulo 'reservas_equipo'
# Solución:
python manage.py migrate

# Problema: Puerto 8000 ya en uso
# Solución:
python manage.py runserver 8001

# Problema: Cambios en templates no se ven
# Solución:
# DEBUG=True ya actualiza automáticamente
# Si no, reinicia servidor

# Problema: "Table reservas_equipo_reserva doesn't exist"
# Solución:
python manage.py migrate

# Problema: Conflictos en migrations
# Solución:
git checkout --ours reservas_equipo/migrations/0001_initial.py
python manage.py migrate

# Problema: Credenciales olvidadas
# Solución:
python manage.py createsuperuser
```

---

## 📊 Estructura de URLs del Proyecto

```
/ 
├── admin/                    # Panel administrativo
├── auth/
│   ├── login/               # Iniciar sesión
│   └── logout/              # Cerrar sesión
└── reservas/
    ├── (lista de reservas)
    ├── nueva/               # Crear nueva reserva
    ├── <id>/                # Detalle de reserva
    ├── <id>/editar/         # Editar reserva
    └── <id>/eliminar/       # Eliminar reserva
```

---

## 📦 Estructura de Archivos Importante

```bash
# Archivos que NO subir a Git:
venv/                       # Entorno virtual
*.pyc                       # Archivos compilados
__pycache__/               # Cache de Python
db.sqlite3                 # Base de datos local
.env                       # Variables de entorno
*.log                      # Archivos de log

# Archivos que SÍ subir:
manage.py
requirements.txt
README.md
TRABAJO_EN_EQUIPO.md
reservas_equipo/           # Código
templates/                 # Templates
static/                    # CSS, JS, imágenes
```

---

## 🚀 Deploy a Producción (Futuro)

```bash
# Cuando sea momento de publicar:

# 1. Crear archivo .env
SECRET_KEY=tu-clave-secreta
DEBUG=False
ALLOWED_HOSTS=tudominio.com

# 2. Collecionar estáticos
python manage.py collectstatic --noinput

# 3. Ejecutar gunicorn
gunicorn reservas_lab_equipo.wsgi

# 4. Configurar Nginx como reverse proxy
# (Ver documentación de Nginx)
```

---

**Tip:** Guarda este archivo en favoritos. Lo usarás cada día. ⭐
