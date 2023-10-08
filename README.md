# Simple Task Manager
[TOC]

### Requisitos 

Diseñar un gestor de tareas simple en Django, que permitiese asignar imágenes a las tareas y que éstas se almacenaran en un bucket de S3. El sistema debe tener el acceso restringido y permitir la búsqueda por título de la tarea y estado.  La aplicación permitirá acceso mediante navegador y mediante el cosumo de su API.

### Descripción de la solución 

Para implementar la solución he utilizado Django Rest Framework ya que proporciona mecanismos muy potentes para la gestión de apis. La estructura y arquitectura de este diseño, no tiene la estructura ni las características que suelen utilizarse generalmente en Django ya que la experiencia y los años me han enseñado que determinadas cualidades del framework, suelen ser malentendidas o utilizadas de manera descuidada afectando a la mantenibilidad del sistema. Por eso , aunque no se solicitaba explícitamente en los requisitos, He implementado un diseño de arquitectura propio desarrollado con el objetivo de minimizar el acoplamiento y favoreciendo la reutilización y aislamiento de la lógica de negocio. Implementado con bastante éxito en los últimos proyectos en los que he trabajado.



#### Estructura de directorios 

La aplicación cuenta con la siguiente estructura de directorios cuyas características explicaré brevemente.

##### /docker/ 

Contiene el dockerfile encargado de generar la imagen del proyecto.

##### /app/ 

contiene la estructura de la aplicación   

##### /app/backend/

El directorio *backend* es el directorio más importante de la aplicación ya que es el que contiene la lógica de negocio y se encarga del acceso a los datos. Por norma general y salvo excepciones forzosas ningún otra aplicación puede acceder a la base de datos de ninguna forma. Es en esta aplicación donde se definen modelos , servicios etc...

##### /app/api/

Como su nombre indica  el directorio *api* contiene todos los elementos que permiten exponer una api para interactuar con la aplicación. Es dentro de éste directorio donde se encontrarán prácticamente todas las referencias a elementos de Django Rest Framework. Fuera de éste directorio solo backend podrá acceder a modelos (exclusivamente) de DRF, con el objetivo de poder proporcionar los servicios necesarios a la api. Esta aplicación se limita a propocionar una capa de interacción con el usuario recibiendo su petición y enviando su respuesta, pero sin contener lógica de negocio.

##### /app/frontend/

Es la aplicación encargada de exponer las vistas que permitirán utilizar un frontend web para interactuar con la aplicación. De la misma forma que sucede con la api, esta aplicación se limita a definir las vistas y las plantillas necesarias par mostrar la interfaz de usuario, pero no contiene lógica de negocio.

##### /app/project/

Es el directorio que contiene los archivos de configuración de Django y el módulo wsgi. En el caso de esta aplicación de pruebas el módulo es sencillo por lo que solo contiene un archivo settings. 



#### Decisiones de diseño 

Al implementar este diseño compartimentado donde el grueso del trabajo cae sobre la aplicación *backend*, he tenido varios objetivos en mente. Por un lado , al unificar toda la lógica de negocio en un solo lugar, evitamos las duplicidades accidentales típicas de los proyectos de Django donde la mísma lógica puede estar contenida en una vista, un formulario, un serializador , una tarea de celery ... 

Django ya aconseja algo similar en su documentación cuando nos aconseja tener modelos "gordos " y vistas "delgadas", pero en mi experiencia, esa aproximación plantea algunos problemas de escalabildad complejos de resolver. Por un lado los modelos acaban siendo demasiado grandes y en ocasiones inmanejables y por otro lado surgen dudas sobre quien debe tener la lógica de negocio cuando un modelo hace referencia a modelos de otras aplicaciones y acabamos acoplando modelos entre ellos y con más frecuencia de la que nos gusta admitir... introduciendo referencias circulares.

Por último, el objetivo de los servicios es hacer que la implementación de test sea más simple. para ello el objetivo es reducir la responsabilidad del resto de elementos de Django al mínimo (Vistas, Apis, Modelos, Formulario, Serializadores...).

Con esta arquitectura establecemos unos "limites" o "fronteras" entre las diferentes partes del sistema que solo podremos traspasar a través del uso de servicios. 

##### Elementos del diseño 

Como he mencionado anteriormente, el grueso de la funcionalidad recae en el backend limitando la responsabilidad del resto de elementos tal y cono se describe 

- **Vistas y API** : Su única responsabilidad será la de procesar la entrada del usuario y devolver una respuesta, controlando el acceso y llamando al servicio correspondiente  transformando  posteriormente la respueta en el formato apropiado ( ya sea mediante serializdador o renderizando la plantilla). No tienen permitido acceder a modelos, realizar consultas, validar restricciones de negocio (solo de login).
- Formularios y serializadores : Reduciremos la funcionalidad de formularios y serializadores a ser los que definen los datos de entrada esperados y los encargados de, mediante validaciones simples, determinar si son válidos o no. En ningun caso , los formularios o serializadores realizarán validaciones complejas que tengan que ver con la Lógica de negocio. Tampoco tiene permitido acceder a base de datos para guardar los datos mediante save
- **Modelos**: Los modelos permanecen con su funcionalidad normal , con la única restriccion de que, entre sus métodos o propiedades, no pueden contener operaciones que realicen validaciones de negocio y tampoco que interactúen con otros modelos.
- **Servicios** : Es en los servicios donde recae todo el peso de la lógica de negocio. El servicio es el encargado de validar la entrada con respecto a las reglas de negocio, realizar las operaciones de acceso a datos y , en caso de ser necesario, devolver la información solicitada. En este proyecto puede parecer que los servicios son métodos de un modelo, que hemos desplazado y colocado en otro lugar, pero en realidad, un servicio no tiene por que estar asociado a un único modelo, es más, en aplicaciones donde se combinan varios modelos diferentes para dar un servicio determinado, ésta capa de servicios puede estar dentro de una aplicación que no tiene modelos propios (por ejemplo imaginemos una aplicación *dashboard* que muestra info de todas las aplicaciones, esta aplicación no tendría modelos propios pero si servicios.) . Además esta capa de servicios es la que, en principio, puede tener acceso a otros servicios de aplicaciones funcionando como un "puerto" de conexión entre las apps del proyecto. Los servicios deben ser lo más atómicos y ortogonales posibles para poder combinarse entre ellos.

##### Algunas Ventajas de esta arquitectura 

- Reducir al mínimo la responsabilidad de los serializadores, los formularios y los modelos , hace que escribir test para ellos sea casi innecesario ya que no se salen de la funcionalidad para la que fueron desarrollados (en la mayoria de los casos su funcionalidad queda probada al probar las vistas o las apis)
- El uso de servicios en aplicaciones separadas de las capas de presentación o de las tareas programadas, nos permite tener aplicaciones más pequeñas u manejables sin un sinfin de archivos y acoplamientos a diferentes frameworks o herramientas (Django rest framework, Celery ...)
- Al unificar la lógica en los servicios e independizar sus dependencias podemos reutilizarlos en diferentes lugares sin añadir complejidad al sistema o tener que volver a desarrollar test. 
- Las limitaciones en el uso de serializadores evita que se reutilicen de forma erronea o innecesaria. 
- Es más fácil e intuitivo saber el lugar donde colocar un elemento. 
- Eliminar funcionalidades innecesarias es menos complejo que en una arquitectura Django regular.

##### Principios de diseño aplicados a la solución 

Algunos principios de diseño que he intentao respetar al desarrollar esta solución ha sido 

- KISS: Intentando que, aunque algunas partes no sean las más elegantes se mantengan simples 
- Ley de Demeter: intentando que ningun elemento interacture con objetos o elementos que no son colaboradores directos.
- Responsabilidad única: Intentando que cada elemento sea lo más pequeño posible y que cumpla con una única responsabilidad

### Puesta en marcha 

##### Configurar variables de entorno 

lo primero que debemos hacer para poder arrancar la aplicación es configurar las variables de entorno. para ello debemos copiar el archivo */app/.env.orig* en un archivo .env y sustituir los valores de las variables de entorno definidas, por valores reales . El archivo contiene las siguientes variables de entorno 

```bash
SECRET_KEY=""
ALLOWED_HOSTS="*"
DEBUG=True
DATABASE_HOST=db
DATABASE_NAME=tasks_manager_db
DATABASE_USER=tasks_manager_user
DATABASE_PASSWORD=tasks_manager_pass
DATABASE_PORT=5432
USE_S3=True
AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
AWS_STORAGE_BUCKET_NAME=""
```



##### Arrancar la imagen de docker 

```bash
docker compose up --build
```



##### Inicializar los datos de pruebas 

Para ello, debemos acceder al contenedor, ya sea desde una interfáz gráfica o desde consola mediante 

```bash
docker exec -it tasks_manager_web_1 s
```

Una vex en el contenedor ejecutamos el siguiente comando 

```
python manage.py shell < scripts/initialize_data.py
```

El script creará un usuario demo con acceso a través de api y algunas tareas de prueba.



##### Acceso a la interfaz web

El acceso a la interfaz web se realiza mediante http://localhost:9000  con el contenedor en ejecución. 



### Documentación de la API 

La documentación de la api y los ejemplos de acceso a los diferentes endpoints se encuentan en el archivo /scripts/endpoints_demo.py




##### Listado de Tareas  -  `GET /api/v1/tasks/list`

*Descripción*: Este endpoint devuelve la lista de tareas existentes.

*Datos de Entrada:*  No requiere datos de entrada.

*Respuesta:*  200-OK -  Devuelve una lista de tareas en formato JSON. 

```json
[
{'uuid': 'uuid de la tarea', 
 'title': 'título de la tarea', 
 'created': '07-10-2023 23:32:50', 
 'expires': '07-10-2023', 
 'status': 'pending'
},]
 
```

#### Crear Tarea: `POST /api/v1/tasks/create`

*Descripción*: Crea una nueva tarea con los datos proporcionados.

*Datos de Entrada*:

- `title` (str): Título de la tarea.
- `description` (str): Descripción de la tarea.
- `expires` (str): Fecha de vencimiento de la tarea en formato YYYY-MM-DD.
- `status` (str): Estado de la tarea (por ejemplo, "pendiente" o "completada").

*Respuesta*:  201- CREATED  



##### Actualizar Tarea  `PUT /api/v1/tasks/update/{task_uuid}`

*Descripción*: Actualiza los detalles de una tarea existente identificada por su `task_uuid`.

*Datos de Entrada*:

- `task_uuid` (str): UUID único de la tarea que se desea actualizar (va en la url).
- `title` (str): Nuevo título de la tarea.
- `description` (str): Nueva descripción de la tarea.
- `expires` (str): Nueva fecha de vencimiento de la tarea en formato YYYY-MM-DD.
- `status` (str): Nuevo estado de la tarea.

*Respuesta:*  204- No Content



##### Eliminar Tarea  `DELETE /api/v1/tasks/delete/{task_uuid}`

*Descripción*: Elimina una tarea existente identificada por su `task_uuid`.

*Datos de Entrada*:

- `task_uuid` (str): UUID único de la tarea que se desea eliminar.

*Respuesta*: Devuelve un mensaje de éxito si la tarea ha sido eliminada correctamente.



### Carencias y posibles mejoras 

- Todas las APIs comparten estructura similar, lo que podría unificarse en una clase base, haciendo así que los mensajes que se envian al usuario queden unificados 
- Las vistas tambien comparten la misma estructura por lo que se podría aplicar una solución similar a las de las apis 
- Se podrian internacionalizar tanto las vistas y apis como las plantillas para traducir los textos a diferentes idiomas. 
- Las imágenes pueden comprimirse al subirse a AWS para evitar malgastar almacenamiento y reducir costes 
- Todas las respuetas de errores tienen la misma estructura por lo que podrían refactorizarse en su propia clase.
- Documentación de la API mediante alguna herramienta automática como SwaggerUI



#### Disclaimer y conclusiones finales

El diseño de ésta arquitectura no ha sido hecho de 0 por mi. El diseño de esta arquitectura es la combinación de elementos de otros autores de los que he tomado aquellas partes que creí resolverían el problema que estábamos teniendo en el proyecto. Aunque esta arquitectura me ha dado muy buen resultado (mucho mejor de lo que esperaba), aún tiene carencias en determinadas situaciones que no encajan del todo con ella , por lo que no es una solución universal que encajar en cualquier proyecto.  Existen muchos proyectos en los que la arquitectura tradicional de Django son una mejor opción (en este proyecto simple seguramente lo era). 



#### Bibliografia y fuentes de insiparción 

Como he mencionado, el diseño de esta arquitectura es la combinación y recopilación de conocimientos de otros autores ;

 La guía de estilo de Django desarrollado por HackSoftware , que me dio la idea de la limitación de funcionalidades y de como mejorar el uso que hacía de los servicios, se puede consultar en  https://github.com/HackSoftware/Django-Styleguide . 

También he aplicado consejos y conocimiento adquiridos de los libros ,

 *Código sostenible* (Carlos Blé Jurado) 

 *La artesanía del código limpio* - Robert C. Martin (libro)



