[TOC]

# Documentación de la API

## Autenticación
Para acceder a la API, es necesario autenticarse utilizando el siguiente punto final:

**Endpoint:** `/api/v1/auth/token/`

**Método:** `POST`

**Cuerpo de la Solicitud:**
- `username` (cadena): Nombre de usuario del usuario.
- `password` (cadena): Contraseña del usuario.

**Respuesta:**
- Código de Estado: 200 OK
- Cuerpo: Un objeto JSON que contiene el token de autenticación del usuario.

---

## Tareas

### Listar Tareas
Recupera una lista paginada de tareas de la base de datos.

**Endpoint:** `/api/v1/tasks/list/`

**Método:** `GET`

**Cabeceras de la Solicitud:**
- `Authorization`: Token para acceder a la API.

**Respuesta:**
- Código de Estado: 200 OK
- Cuerpo: Una lista paginada que contiene diccionarios con las siguientes claves:
  - `uuid` (cadena): UUID de la tarea.
  - `title` (cadena): Título de la tarea.
  - `created` (cadena): Marca de tiempo que indica el momento de creación de la tarea.
  - `expires` (cadena): Fecha de vencimiento de la tarea.
  - `status` (cadena): Estado de la tarea.

---

### Crear Tarea
Crea una nueva tarea en la base de datos.

**Endpoint:** `/api/v1/tasks/create/`

**Método:** `POST`

**Cabeceras de la Solicitud:**
- `Authorization`: Token para acceder a la API.

**Cuerpo de la Solicitud:**
- `title` (cadena): Título de la tarea.
- `description` (cadena): Descripción de la tarea.
- `expires` (cadena): Fecha de vencimiento de la tarea.
- `status` (cadena): Estado de la tarea.

**Respuesta:**
- Código de Estado: 201 Created
- Cuerpo: Un objeto JSON que contiene el UUID de la tarea creada.

---

### Actualizar Tarea
Actualiza una tarea existente en la base de datos.

**Endpoint:** `/api/v1/tasks/update/{task_uuid}/`

**Método:** `PUT`

**Cabeceras de la Solicitud:**
- `Authorization`: Token para acceder a la API.

**Cuerpo de la Solicitud:**
- `title` (cadena): Título actualizado de la tarea.
- `description` (cadena): Descripción actualizada de la tarea.
- `expires` (cadena): Fecha de vencimiento actualizada de la tarea.
- `status` (cadena): Estado actualizado de la tarea.

**Respuesta:**
- Código de Estado: 204 No Content

---

### Eliminar Tarea
Elimina una tarea de la base de datos.

**Endpoint:** `/api/v1/tasks/delete/{task_uuid}/`

**Método:** `DELETE`

**Cabeceras de la Solicitud:**
- `Authorization`: Token para acceder a la API.

**Respuesta:**
- Código de Estado: 204 No Content

---

## Imágenes de Tareas

### Crear Imagen de Tarea
Crea una nueva imagen asociada a una tarea.

**Endpoint:** `/api/v1/tasks/image/create/{task_uuid}/`

**Método:** `POST`

**Cabeceras de la Solicitud:**
- `Authorization`: Token para acceder a la API.

**Cuerpo de la Solicitud:**
- `image` (archivo): El archivo de imagen que se va a subir.
- `image_type` (cadena): Tipo de la imagen (por ejemplo, 'image/jpeg' o 'image/png').

**Respuesta:**
- Código de Estado: 201 Created
- Cuerpo: Un objeto JSON que contiene la URL de la imagen creada.

---

### Listar Imágenes de Tarea
Enumera las imágenes asociadas a una tarea específica.

**Endpoint:** `/api/v1/tasks/image/list/{task_uuid}/`

**Método:** `GET`

**Cabeceras de la Solicitud:**
- `Authorization`: Token para acceder a la API.

**Respuesta:**
- Código de Estado: 200 OK
- Cuerpo: Una lista de diccionarios. Cada diccionario contiene las siguientes claves:
  - `uuid` (cadena): UUID de la imagen.
  - `image` (cadena): URL de la imagen.

---

### Eliminar Imagen de Tarea
Elimina la imagen con el UUID especificado.

**Endpoint:** `/api/v1/tasks/image/delete/{image_uuid}/`

**Método:** `DELETE`

**Cabeceras de la Solicitud:**
- `Authorization`: Token para acceder a la API.

**Respuesta:**
- Código de Estado: 204 No Content

---

### Función Auxiliar: Encabezado de Autenticación
Genera el encabezado de autenticación con el token proporcionado.

**Función:**
```python
def auth_header(token: str) -> dict:
    """
    Genera el encabezado de autenticación con el token proporcionado.
    
    Args:
        token (cadena): Token de autorización.
    
    Returns:
        dict: Un diccionario que contiene el encabezado de autorización.
    """
    return {"Authorization": f"Token {token}"}
