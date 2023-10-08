import requests

BASE_API_URL = "http://localhost:9000/api/v1/%(endpoint_path)s/"

"""
Endpoint de autenticación para obtener el token del usuario.
"""


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


class TasksAPIExamples:
    API_URL = "http://localhost:9000/api/v1/tasks/%(endpoint_path)s/"

    def get_endpoint_url(self, endpoint_path: str) -> str:
        return self.API_URL % {"endpoint_path": endpoint_path}

    def __init__(self, api_token):
        self._api_token = api_token
        self._auth_headers = auth_header(self._api_token)

    def list_tasks(self) -> dict:
        url = self.get_endpoint_url("list")
        response = requests.get(url, headers=self._auth_headers)
        return response.json()

    def create_task(self, title: str, description: str, expires: str, status: str):
        post_data = {
            "title": title,
            "description": description,
            "expires": expires,
            "status": status,
        }

        url = self.get_endpoint_url("create")
        return requests.post(url, headers=self._auth_headers, data=post_data)

    def update_task(
        self, task_uuid: str, title: str, description: str, expires: str, status: str
    ):
        post_data = {
            "title": title,
            "description": description,
            "expires": expires,
            "status": status,
        }

        url = self.get_endpoint_url(f"update/{task_uuid}")
        return requests.put(url, headers=self._auth_headers, data=post_data)

    def delete_task(
        self,
        task_uuid: str,
    ):
        url = self.get_endpoint_url(f"delete/{task_uuid}")
        return requests.delete(url, headers=self._auth_headers)


if __name__ == "__main__":
    token = login()
    tasks_api = TasksAPIExamples(token)
    # tasks_api.list_tasks()
    # # tasks_api.create_task(
    # #     "Mi new created task from console", "lorem ipsum", "2023-12-12", "pending"
    # # )

    # tasks_api.update_task(
    #     "370d4dce-4268-4935-beed-70c65ef91a72",
    #     "Mi updated task and completed",
    #     "lorem ipsum",
    #     "2023-12-12",
    #     "completed",
    # )

    tasks_api.delete_task("370d4dce-4268-4935-beed-70c65ef91a72")
