# Daily Planner

Aplicación web desarrollada con Django para la planificación diaria de actividades. Permite organizar tareas en franjas horarias, mantener un checklist global con niveles de urgencia, adjuntar archivos y crear sub-tareas.

## Funcionalidades

| Funcionalidad | Detalle |
|---------------|---------|
| **Planificador horario** | Organiza tu jornada en franjas de 7:00 a 19:00 |
| **CRUD de tareas** | Crear, editar y eliminar tareas en cada franja horaria |
| **Adjuntar archivos** | Sube imágenes y capturas de pantalla a cada tarea (soporte para pegar con Ctrl+V) |
| **Checklist global** | Lista de tareas pendientes/completadas con nivel de urgencia (1=Muy urgente a 5=Informativo) |
| **Sub-tareas** | Fragmentos detallados dentro de cada checklist (ideal para consultas SQL o pasos complejos) |
| **Filtros** | Búsqueda por texto y filtro por usuario en el checklist global |
| **Autenticación** | Sistema de login/logout con protección multi-usuario |

## Stack tecnológico

- **Backend:** Django 6.0, Python 3.12
- **Base de datos:** SQLite
- **Frontend:** Bootstrap 5.3, Bootstrap Icons
- **Autenticación:** django.contrib.auth

## Estructura del proyecto

```
ProyectoPlanner-main/
├── dayplanner/                  # Configuración del proyecto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── planner/                     # App principal
│   ├── models.py                # Day, HourSlot, Task, TaskAttachment, ChecklistItem, SubChecklistItem
│   ├── views.py                 # Lógica de negocio
│   ├── forms.py                 # Formularios
│   ├── urls.py                  # Rutas
│   ├── context_processors.py    # Context processor para checklist global
│   └── templates/planner/       # Plantillas HTML (base, index, day_view, task_form, etc.)
├── media/                       # Archivos subidos por usuarios
├── static/                      # Archivos estáticos
├── manage.py
└── requirements.txt
```

## Instalación y uso

### Requisitos

- Python 3.10+
- pip

### Pasos

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd ProyectoPlanner-main

# Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Migrar base de datos
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

Abrir http://127.0.0.1:8000 e iniciar sesión.

## Modelos principales

- **Day** — Día del planificador (vinculado a un usuario)
- **HourSlot** — Franja horaria de 1 hora (7:00 a 19:00)
- **Task** — Tarea dentro de una franja horaria
- **TaskAttachment** — Archivo adjunto a una tarea
- **ChecklistItem** — Elemento del checklist global con nivel de urgencia
- **SubChecklistItem** — Sub-elemento detallado dentro de un checklist
