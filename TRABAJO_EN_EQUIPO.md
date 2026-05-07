# 👥 Guía de Trabajo en Equipo - SantyTeam

## 📋 Distribución de Responsabilidades

### **Integrante 1: Módulo de Autenticación**
**Responsable por:**
- Autenticación (login/logout)
- Gestión de roles
- Permisos y seguridad

**Archivos a modificar:**
```
reservas_equipo/
  ├── views.py (LoginView, LogoutView)
  ├── forms.py (LoginCustomForm)
  ├── urls/auth.py
  └── models.py (agregar campos de rol a User si es necesario)

templates/
  ├── auth/login.html
  └── base/navbar.html (íconos de usuario)

static/
  └── css/style.css (si necesita estilos especiales)
```

**Tareas iniciales:**
- [ ] Verificar que login funcione correctamente
- [ ] Agregar mensajes de error personalizados
- [ ] Implementar "Recordarme"
- [ ] Validar roles de usuario (docente/admin)

---

### **Integrante 2: Módulo de CRUD Reservas**
**Responsable por:**
- Crear reservas
- Editar reservas
- Eliminar reservas
- Validaciones de conflictos

**Archivos a modificar:**
```
reservas_equipo/
  ├── views.py (ReservaCreateView, UpdateView, DeleteView)
  ├── forms.py (ReservaForm)
  ├── models.py (validaciones en method clean)
  └── urls/reservas.py

templates/reservas/
  ├── reserva_form.html
  └── reserva_confirm_delete.html
```

**Tareas iniciales:**
- [ ] Probar que se creen reservas
- [ ] Validar que hora_fin > hora_inicio
- [ ] Validar que no haya conflictos de horarios
- [ ] Probar edición de reservas pendientes
- [ ] Probar eliminación de reservas pendientes

---

### **Integrante 3: Módulo de Listado y Filtros**
**Responsable por:**
- Listado de reservas
- Filtros avanzados
- Búsqueda
- Detalle de reserva

**Archivos a modificar:**
```
reservas_equipo/
  ├── views.py (ReservaListView, DetailView)
  ├── forms.py (FiltroReservasForm)
  └── urls/reservas.py

templates/reservas/
  ├── reserva_list.html
  ├── reserva_detail.html
```

**Tareas iniciales:**
- [ ] Probar filtrado por laboratorio
- [ ] Probar filtrado por estado
- [ ] Probar filtrado por fecha
- [ ] Probar paginación
- [ ] Probar detalle de reserva

---

### **Integrante 4: Módulo de Admin y Estadísticas**
**Responsable por:**
- Panel de administración
- Estadísticas
- Dashboard

**Archivos a modificar:**
```
reservas_equipo/
  ├── admin.py (completo)
  ├── views.py (HomeView - estadísticas)
  └── models.py (agregar métodos de query)

templates/
  ├── home.html (estadísticas)
  └── base/navbar.html (enlace admin)

static/
  ├── css/style.css (estilos dashboard)
  └── js/ (gráficos - opcional)
```

**Tareas iniciales:**
- [ ] Verificar que admin funcione
- [ ] Agregar filtros a admin
- [ ] Crear usuarios de prueba
- [ ] Generar laboratorios de prueba
- [ ] Mostrar estadísticas en home

---

## 🔄 Flujo de Trabajo Diario

### **Mañana (Inicio de sesión)**
```bash
# 1. Actualizar código desde develop
git checkout develop
git pull origin develop

# 2. Cambiar a tu rama feature
git checkout feature/<tu-módulo>

# 3. Si develop tiene cambios nuevos, mergebiar
git merge develop
# (Resolver conflictos si los hay)
```

### **Durante el día**
```bash
# 1. Hacer cambios en tus archivos
# 2. Ver qué cambió
git status

# 3. Agregar tus cambios
git add .

# 4. Commit con mensaje claro
git commit -m "feat(auth): validar rol de usuario"
# O "fix(reservas): resolver conflicto de horarios"

# 5. Ver commit log
git log --oneline

# 6. Enviar a GitHub
git push origin feature/<tu-módulo>
```

### **Antes de terminar**
```bash
# 1. Asegurarse que todo funciona
python manage.py test

# 2. Push final
git push origin feature/<tu-módulo>

# 3. Crear Pull Request en GitHub
```

---

## 🚨 Cómo Evitar Conflictos

### **Conflicto 1: Dos personas modifican mismo archivo**

```bash
# MALO ❌
# Integrante 1 y 2 modifican views.py al mismo tiempo

# BUENO ✅
# Integrante 1 modifica views.py:100-150 (LoginView)
# Integrante 2 modifica views.py:200-300 (ReservaCreateView)
# No hay conflicto porque tocan secciones diferentes
```

**Solución si hay conflicto:**
```bash
git status
# Verás archivos con "both modified"

# Abrir el archivo y ver:
# <<<<<<<< feature/auth
#   código de integrante 1
# ========
#   código de integrante 2
# >>>>>>>> feature/reservas-crud

# Resolver manualmente, luego:
git add .
git commit -m "fix: resolver conflicto en views.py"
```

### **Conflicto 2: Modificar settings.py o models.py**

```bash
# AVISO: Estos archivos son críticos

# ANTES de hacer cambios, avisa al equipo:
# "Voy a agregar un campo a Reserva"

# Hazlo en una rama separada:
git checkout -b feature/nuevo-campo-reserva

# Hazlo, commit y crea PR
# El equipo revisa antes de mergebiar
```

---

## 🧪 Checklist Antes de Hacer Push

- [ ] Mi código funciona localmente
- [ ] No rompí nada en otras secciones
- [ ] Probé los cambios múltiples veces
- [ ] Hice commit con mensaje claro
- [ ] Incluí comentarios en código complicado
- [ ] No agregué archivos innecesarios
- [ ] Mi rama está actualizada con develop

```bash
# Checklist automatizado:
python manage.py runserver  # ¿Funciona?
git status                  # ¿Hay cambios no commiteados?
git log --oneline -5        # ¿Mensajes claros?
git push origin feature/<tu-módulo>  # Push
```

---

## 🔍 Revisión de Código (Code Review)

### **Cuando hagas Pull Request:**

1. **Describe qué hiciste:**
   ```
   # Título
   feat(auth): validar que solo admin puede aprobar
   
   # Descripción
   - Agregué permiso de admin a ReservaUpdateView
   - Validé roles en models.py
   - Agregué test para roles
   
   # Testing
   - ✅ Login funciona
   - ✅ Solo admin ve opción de aprobar
   - ✅ User regular no puede aprobar
   ```

2. **Espera a que alguien revise**
3. **Responde comentarios**
4. **Haz cambios si son sugeridos**
5. **Aprueba y mergebía**

---

## 📊 Cómo Probar tu Módulo

### **Antes de hacer commit:**

```bash
# 1. Abrir Django shell
python manage.py shell

# 2. Crear datos de prueba
>>> from django.contrib.auth.models import User
>>> from reservas_equipo.models import Laboratorio, Reserva
>>> 
>>> # Crear usuario
>>> user = User.objects.create_user('docente', 'docente@test.com', 'pass123')
>>> user.first_name = 'Juan'
>>> user.save()
>>>
>>> # Crear laboratorio
>>> lab = Laboratorio.objects.create(nombre='Lab 1', capacidad=30)
>>>
>>> # Crear reserva
>>> from datetime import date, time
>>> res = Reserva.objects.create(
...     usuario=user,
...     laboratorio=lab,
...     fecha=date.today(),
...     hora_inicio=time(9, 0),
...     hora_fin=time(10, 0),
...     motivo='Clase',
...     estado='pendiente'
... )

# 3. Probar en navegador
# http://localhost:8000/
# http://localhost:8000/auth/login/
# http://localhost:8000/reservas/
```

---

## 🐛 Comandos Útiles para Debugging

```bash
# Ver estado del proyecto
git status
git log --oneline

# Ver diferencias
git diff                    # Cambios no stagiados
git diff --staged          # Cambios stagiados
git diff feature/auth..develop  # Diferencia entre ramas

# Deshacer cambios
git checkout -- archivo.py  # Deshacer un archivo
git reset HEAD~1           # Deshacer último commit
git revert <commit>        # Crear commit que revierte cambios

# Limpiar rama
git clean -fd              # Eliminar archivos sin track
git reset --hard           # Volver a último commit (PELIGRO)

# Django
python manage.py migrate   # Aplicar migraciones
python manage.py shell     # Consola Django
python manage.py test      # Ejecutar tests
```

---

## 📞 Plan de Comunicación

### **Reunión Diaria (5 min)**
- Qué hizo cada uno
- Qué va a hacer
- Bloqueos/problemas

### **Reunión de Integración (Viernes)**
- Merger feature branches a develop
- Code review entre pares
- Resolver conflictos

### **Documentar en Issues**
- Bugs encontrados
- Tareas pendientes
- Ideas nuevas

---

## ✅ Checklist de Entrega

Antes de considerar el proyecto completo:

- [ ] Todas las ramas feature merged a develop
- [ ] develop está actualizado y funciona
- [ ] No hay bugs conocidos
- [ ] Código tiene comentarios
- [ ] README está actualizado
- [ ] Se probó en múltiples navegadores
- [ ] Se probó con múltiples usuarios
- [ ] Hay datos de prueba en BD
- [ ] Admin funciona correctamente
- [ ] No hay crasheos

---

**¡Éxito con el proyecto! 🚀**
