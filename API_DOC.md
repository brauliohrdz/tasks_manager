[TOC]

# API Documentation

## Authentication
To access the API, you need to authenticate using the following endpoint:

**Endpoint:** `/api/v1/auth/token/`

**Method:** `POST`

**Request Body:**
- `username` (string): User's username.
- `password` (string): User's password.

**Response:**
- Status Code: 200 OK
- Body: A JSON object containing the user's authentication token.

---

## Tasks

### List Tasks
Retrieves a list of tasks from the database.

**Endpoint:** `/api/v1/tasks/list/`

**Method:** `GET`

**Request Headers:**
- `Authorization`: Token for API access.

**Response:**
- Status Code: 200 OK
- Body: A dictionary containing the list of tasks obtained from the API.

---

### Create Task
Creates a new task in the database.

**Endpoint:** `/api/v1/tasks/create/`

**Method:** `POST`

**Request Headers:**
- `Authorization`: Token for API access.

**Request Body:**
- `title` (string): Title of the task.
- `description` (string): Description of the task.
- `expires` (string): Expiry date of the task.
- `status` (string): Status of the task.

**Response:**
- Status Code: 201 Created
- Body: A JSON object containing the UUID of the created task.

---

### Update Task
Updates an existing task in the database.

**Endpoint:** `/api/v1/tasks/update/{task_uuid}/`

**Method:** `PUT`

**Request Headers:**
- `Authorization`: Token for API access.

**Request Body:**
- `title` (string): Updated title of the task.
- `description` (string): Updated description of the task.
- `expires` (string): Updated expiry date of the task.
- `status` (string): Updated status of the task.

**Response:**
- Status Code: 204 No Content

---

### Delete Task
Deletes a task from the database.

**Endpoint:** `/api/v1/tasks/delete/{task_uuid}/`

**Method:** `DELETE`

**Request Headers:**
- `Authorization`: Token for API access.

**Response:**
- Status Code: 204 No Content



## Task Images

### Create Task Image
Creates a new image associated with a task.

**Endpoint:** `/api/v1/tasks/image/create/{task_uuid}/`

**Method:** `POST`

**Request Headers:**
- `Authorization`: Token for API access.

**Request Body:**
- `image` (file): The image file to be uploaded.
- `image_type` (string): Type of the image (e.g., 'image/jpeg' or 'image/png').

**Response:**
- Status Code: 201 Created
- Body: A JSON object containing the URL of the created image.

---

### List Task Images
Lists images associated with a specific task.

**Endpoint:** `/api/v1/tasks/image/list/{task_uuid}/`

**Method:** `GET`

**Request Headers:**
- `Authorization`: Token for API access.

**Response:**
- Status Code: 200 OK
- Body: A dictionary containing the list of images associated with the task.

---

### Delete Task Image
Deletes the image with the specified UUID.

**Endpoint:** `/api/v1/tasks/image/delete/{image_uuid}/`

**Method:** `DELETE`

**Request Headers:**
- `Authorization`: Token for API access.

**Response:**
- Status Code: 204 No Content

---

### Helper Function: Authentication Header
Generates the authentication header with the provided token.

**Function:**
```python
def auth_header(token: str) -> dict:
    """
    Generates the authentication header with the provided token.
    
    Args:
        token (str): Authorization token.
    
    Returns:
        dict: A dictionary containing the authorization header.
    """
    return {"Authorization": f"Token {token}"}