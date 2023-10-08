import os

import requests

BASE_API_URL = "http://localhost:9000/api/v1/%(endpoint_path)s/"


def login() -> str:
    """
    Realiza una solicitud de autenticación para obtener el token del usuario.

    Esta función envía una solicitud POST a la URL de autenticación especificada
    con credenciales de usuario (nombre de usuario y contraseña). La respuesta
    se espera que esté en formato JSON y debe contener un campo llamado "token"
    que representa el token de autenticación del usuario.

    Returns:
        str: Token de autenticación del usuario obtenido después de la autenticación.

    """
    url = BASE_API_URL % {"endpoint_path": "auth/token"}
    post_data = {"username": "demo", "password": "demo1234"}

    response = requests.post(url, data=post_data)
    return response.json().get("token")


def auth_header(token: str) -> dict:
    """
    El sistema realiza la autenticación por token por lo que todas nuestras peticiones
    tras el login deben incorporar esta cabecera con un token válido
    """
    return {"Authorization": f"Token {token}"}


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TASKS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def list_tasks(token: str) -> dict:
    """
    Obtiene una lista de tareas desde la base de datos y las devuelve como un diccionario.

    Args:
        token (str): Token de autorización para acceder al API.

    Returns:
        dict: Un diccionario que contiene la lista de tareas obtenida del API.
    HTTP Status Codes:
        200 OK: Se devuelve cuando la solicitud se realiza correctamente.
    """
    url = BASE_API_URL % {"endpoint_path": "tasks/list"}
    headers = auth_header(token)
    response = requests.get(url, headers=headers)
    return response.json()


def create_task(token, title: str, description: str, expires: str, status: str) -> str:
    """
    Crea una tarea en la base de datos y devuelve el UUID de la tarea creada.

    Args:
        title (str): Título de la tarea.
        description (str): Descripción de la tarea.
        expires (str): Fecha de vencimiento de la tarea.
        status (str): Estado de la tarea.
        token (str): Token de autorización para acceder al API.

    Returns:
        str: UUID de la tarea creada.

    HTTP Status Codes:
        201 Created: Se devuelve cuando la tarea se crea correctamente.


    """
    post_data = {
        "title": title,
        "description": description,
        "expires": expires,
        "status": status,
    }
    url = BASE_API_URL % {"endpoint_path": "tasks/create"}
    headers = auth_header(token)
    response = requests.post(url, headers=headers, data=post_data).json()
    return response.get("uuid")


def update_task(
    token: str,
    task_uuid: str,
    title: str,
    description: str,
    expires: str,
    status: str,
) -> None:
    """
    Actualiza los datos de la tarea especificada por el UUID dado.

    Args:
        token (str): Token de autorización para acceder al API.
        task_uuid (str): UUID de la tarea que se va a actualizar.
        title (str): Título actualizado de la tarea.
        description (str): Descripción actualizada de la tarea.
        expires (str): Fecha de vencimiento actualizada de la tarea.
        status (str): Estado actualizado de la tarea.

    Returns:
        None

    HTTP Status Codes:
        204 No Content: Se devuelve cuando la tarea se actualiza correctamente.
    """
    put_data = {
        "title": title,
        "description": description,
        "expires": expires,
        "status": status,
    }
    url = BASE_API_URL % {"endpoint_path": f"tasks/update/{task_uuid}"}
    headers = auth_header(token)
    return requests.put(url, headers=headers, data=put_data)


def delete_task(
    token: str,
    task_uuid: str,
) -> None:
    """
    Elimina la tarea con el UUID especificado.

    Args:
        task_uuid (str): UUID de la tarea que se va a eliminar.
        token (str): Token de autorización para acceder al API.

    Returns:
        None

    HTTP Status Codes:
        204 No Content: Se devuelve cuando la tarea se elimina correctamente.
    """
    url = BASE_API_URL % {"endpoint_path": f"tasks/delete/{task_uuid}"}
    headers = auth_header(token)
    return requests.delete(url, headers=headers)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TASKS IMAGES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def task_image_create(
    token: str, task_uuid, image_file_path: str, image_type: str
) -> str:
    """
        Crea una nueva imagen asociada a la tarea.

    Args:
        token (str): Token de autorización para acceder al API.
        task_uuid (str): UUID de la tarea a la que se asociará la imagen.
        image_file_path (str): Ruta del archivo de la imagen en el sistema de archivos local.
        image_type (str): Tipo de la imagen (por ejemplo, 'image/jpeg' o 'image/png').

    Returns:
        str: URL de la imagen creada.

    HTTP Status Codes:
        201 Created: Se devuelve cuando la imagen se crea correctamente.
    """
    url = BASE_API_URL % {"endpoint_path": f"tasks/image/create/{task_uuid}"}
    headers = auth_header(token)
    with open(image_file_path, "rb") as image:
        file_name = os.path.basename(image_file_path)
        post_data = {"image": (file_name, image, image_type)}
        return requests.post(url, files=post_data, headers=headers)


def list_task_images(token: str, task_uuid: str) -> dict:
    """
    Lista las imágenes de una determinada tarea.

    Args:
        token (str): Token de autorización para acceder al API.
        task_uuid (str): UUID de la tarea cuyas imágenes se listarán.

    Returns:
        dict: Un diccionario que contiene las imágenes de la tarea obtenidas del API.

    HTTP Status Codes:
        200 OK: Se devuelve cuando la solicitud se realiza correctamente.
    """
    url = BASE_API_URL % {"endpoint_path": f"tasks/image/list/{task_uuid}"}
    headers = auth_header(token)
    return requests.get(url, headers=headers)


def delete_task_image(token: str, image_uuid: str) -> None:
    """
    Elimina la imagen con el UUID especificado.

    Args:
        token (str): Token de autorización para acceder al API.
        image_uuid (str): UUID de la imagen que se va a eliminar.

    Returns:
        None

    HTTP Status Codes:
        204 No Content: Se devuelve cuando la imagen se elimina correctamente.
    """
    url = BASE_API_URL % {"endpoint_path": f"tasks/image/delete/{image_uuid}"}
    headers = auth_header(token)
    return requests.delete(url, headers=headers)
