from backend.tasks.tests.utils import TaskTestUtils
from django.contrib.auth.models import User

print("> Creando usuario demo:demo con acceso de super usuario")
user = User(username="demo", email="demo@example.com", is_staff=True, is_superuser=True)
user.set_password("demo")
user.save()

print("> Creando tareas de prueba")
TaskTestUtils.create(
    owner_id=user.id,
    title="Tarea Demo 1",
    description="Lorem ipsum dolor sit amet",
    expires="2023-11-10",
    status="pending",
)
TaskTestUtils.create(
    owner_id=user.id,
    title="Tarea Demo 2",
    description="Lorem ipsum dolor sit amet",
    expires="2023-11-10",
    status="in_progress",
)
TaskTestUtils.create(
    owner_id=user.id,
    title="Tarea Demo 3",
    description="Lorem ipsum dolor sit amet",
    expires="2023-11-10",
    status="completed",
)
