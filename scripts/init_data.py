import warnings

from backend.tasks.tests.utils import TaskTestUtils
from django.contrib.auth.models import User

warnings.filterwarnings("ignore", category=RuntimeWarning)
print("> Creando usuario demo:demo con acceso de super usuario")
user = User(username="demo", email="demo@example.com", is_staff=True, is_superuser=True)
user.set_password("demo")
user.save()

print("> Creando tareas de prueba")
# Tarea 1
TaskTestUtils.create(
    owner_id=user.id,
    title="Realizar Presentación",
    description="Preparar diapositivas para la reunión.",
    expires="2023-10-15",
    status="pending",
)

# Tarea 2
TaskTestUtils.create(
    owner_id=user.id,
    title="Llamar al Cliente",
    description="Confirmar detalles del proyecto.",
    expires="2023-10-18",
    status="in_progress",
)

# Tarea 3
TaskTestUtils.create(
    owner_id=user.id,
    title="Revisar Documentación",
    description="Evaluación del informe trimestral.",
    expires="2023-10-20",
    status="completed",
)

# Tarea 4
TaskTestUtils.create(
    owner_id=user.id,
    title="Enviar Facturas",
    description="Facturación para el mes actual.",
    expires="2023-10-22",
    status="pending",
)

# Tarea 5
TaskTestUtils.create(
    owner_id=user.id,
    title="Entrenamiento del Equipo",
    description="Sesión de capacitación sobre nuevas herramientas.",
    expires="2023-10-25",
    status="in_progress",
)

# Tarea 6
TaskTestUtils.create(
    owner_id=user.id,
    title="Preparar Informe Financiero",
    description="Análisis de ingresos y gastos.",
    expires="2023-10-28",
    status="completed",
)

# Tarea 7
TaskTestUtils.create(
    owner_id=user.id,
    title="Reunión de Proyecto",
    description="Discutir el progreso del proyecto con el equipo.",
    expires="2023-10-30",
    status="pending",
)

# Tarea 8
TaskTestUtils.create(
    owner_id=user.id,
    title="Investigación de Mercado",
    description="Analizar tendencias del mercado para nuevos productos.",
    expires="2023-11-02",
    status="in_progress",
)

# Tarea 9
TaskTestUtils.create(
    owner_id=user.id,
    title="Actualizar Sitio Web",
    description="Agregar nuevas características y mejorar la interfaz.",
    expires="2023-11-05",
    status="completed",
)

# Tarea 10
TaskTestUtils.create(
    owner_id=user.id,
    title="Planificación de Evento",
    description="Organizar detalles para la conferencia anual.",
    expires="2023-11-08",
    status="pending",
)

# Tarea 11
TaskTestUtils.create(
    owner_id=user.id,
    title="Entrenamiento de Producto",
    description="Capacitar al equipo de ventas sobre productos nuevos.",
    expires="2023-11-11",
    status="in_progress",
)

# Tarea 12
TaskTestUtils.create(
    owner_id=user.id,
    title="Revisión de Contenidos",
    description="Evaluar materiales para la campaña de marketing.",
    expires="2023-11-14",
    status="completed",
)

# Tarea 13
TaskTestUtils.create(
    owner_id=user.id,
    title="Preparar Propuestas",
    description="Crear propuestas para clientes potenciales.",
    expires="2023-11-17",
    status="pending",
)

# Tarea 14
TaskTestUtils.create(
    owner_id=user.id,
    title="Optimizar SEO del Sitio",
    description="Mejorar el posicionamiento en los motores de búsqueda.",
    expires="2023-11-20",
    status="in_progress",
)

# Tarea 15
TaskTestUtils.create(
    owner_id=user.id,
    title="Organizar Reunión de Equipo",
    description="Coordinar agenda y temas para la reunión semanal.",
    expires="2023-11-23",
    status="completed",
)


print("----------------------------")
print(" Ahora puedes acceder a la demo en http://localhost:9000")
print(" Con el usuario: 'demo' y la contraseña 'demo'")
print("----------------------------")
