# Simple Task Manager
[TOC]

### Descripción de la aplicación

La aplicación es un gestor de tareas muy simple con las siguientes características 

- Permite crear tareas y agregarles múltiples imágenes (por simplicidad, las imágenes se agregan de una en una a las tareas, una vez dicha tarea ha sido creada)

- Las imágenes se almacenan en un bucket de s3

- Permite interactuar a través del navegador o de una API 

- Tiene acceso restringido  (los usuarios solo pueden acceder a sus propias tareas)

- Permite búsqueda por título y por estado 

  



### Descripción de la solución porpuesta

La solución propuesta utiliza un diseño de arquitectura que no es el típico utilizado en Django y Django Rest Framework. El motivo principal de la elección de esta estructura es porque es la que he diseñado e implementado en el proyecto en el que trabajo actualmente y ha dado muy buen resultado. Con este diseño se consigue reducir el acoplamiento , facilitar la implementación de test y mejorar la mantenibilidad, frente a la arquitectura tradicional de Django que , mal utilizada, puede favorecer la deuda técnica en proyectos grandes.



#### Estructura de directorios 

La aplicación cuenta con la siguiente estructura de directorios cuyas características explicaré brevemente.

**/scripts/**
contiene los scripts de utilidad para inicializar datos y utilizar la API.

##### /docker/ 

Contiene el dockerfile encargado de generar la imagen del proyecto.

##### /app/ 

contiene la estructura de la aplicación   

##### /app/backend/

El directorio *backend* es el directorio más importante de la aplicación ya que es el que contiene la lógica de negocio y se encarga del acceso a los datos. Por norma general y salvo excepciones forzosas, ningún otra aplicación puede acceder a la base de datos de ninguna forma. Es en esta aplicación donde se definen modelos , servicios etc...

##### /app/api/

Como su nombre indica  el directorio *api* contiene todos los elementos que permiten exponer una api para interactuar con la aplicación. Es dentro de éste directorio donde se encontrarán prácticamente todas las referencias a elementos de Django Rest Framework. Fuera de éste directorio solo backend podrá acceder a modelos de DRF, con el objetivo de poder proporcionar los servicios necesarios a la api, por ejemplo para obtener un token de usuario. Esta aplicación se limita a proporcionar una capa de interacción con el usuario recibiendo su petición y enviando su respuesta, pero sin contener lógica de negocio.

##### /app/frontend/

Es la aplicación encargada de exponer las vistas que permitirán utilizar un frontend web para interactuar con la aplicación. De la misma forma que sucede con la api, esta aplicación se limita a definir las vistas y las plantillas necesarias par mostrar la interfaz de usuario, pero sus vistas no contiene lógica de negocio. 

##### /app/project/

Es el directorio que contiene los archivos de configuración de Django y el módulo wsgi. En el caso de esta aplicación de pruebas el módulo es sencillo por lo que solo contiene un archivo settings. 



#### Decisiones de diseño 

El diseño propuesto establece una serie de *"frontera"*, entre los diferentes elementos del sistema, que solo se puede traspasar con unas determinadas condiciones y en puntos muy concretos (principalmente los servicios)

Al implementar este diseño modular, donde el grueso del trabajo cae sobre la aplicación *backend*, he tenido varios objetivos en mente. Por un lado, al unificar toda la lógica de negocio en un solo lugar, evitamos las duplicidades accidentales típicas de los proyectos de Django donde la misma lógica puede estar contenida en una vista, un formulario, un serializador , una tarea que se envía a celery ... 

Django ya aconseja algo similar en su documentación cuando nos aconseja tener modelos "gordos " y vistas "delgadas", pero en mi experiencia, esa aproximación plantea algunos problemas de escalabilidad complejos de resolver. Por un lado los modelos acaban siendo demasiado grandes y en ocasiones inmanejables y por otro lado surgen dudas sobre quien debe tener la lógica de negocio cuando un modelo hace referencia a modelos de otras aplicaciones y acabamos acoplando modelos entre ellos y con más frecuencia de la que nos gusta admitir... introduciendo referencias circulares.

Por último, el objetivo de los servicios es hacer que la implementación de test sea más simple ya que busca reducir al mínimo las responsabilidad del resto de elementos de Django (Vistas, Apis, Modelos, Formulario, Serializadores...), haciendo que la necesidad de implementar test para ellos sea muy pequeña y en ocasiones nula.



##### Elementos del diseño 

Como he mencionado anteriormente, el grueso de la funcionalidad recae en el backend limitando la responsabilidad del resto de elementos tal y cono se describe 

- **Vistas y API** : Su única responsabilidad será la de procesar la entrada del usuario y devolver una respuesta, controlando el acceso y llamando al servicio correspondiente  transformando  posteriormente la respueta en el formato apropiado ( ya sea mediante serializdador o renderizando la plantilla). No tienen permitido acceder a modelos, realizar consultas, validar restricciones de negocio.
- **Formularios y serializadores** : Reduciremos la funcionalidad de formularios y serializadores a ser los que definen los datos de entrada esperados y los encargados de, mediante validaciones simples, determinar si son válidos o no. En ningún caso , los formularios o serializadores realizarán validaciones complejas que tengan que ver con la lógica de negocio. Tampoco tiene permitido acceder a base de datos para almacenar datos mediante el uso del método *save*
- **Modelos**: Los modelos permanecen con su funcionalidad normal , con la única restricción de que, entre sus métodos o propiedades, no pueden contener operaciones que realicen validaciones de negocio y tampoco que interactúen con otros modelos.
- **Servicios** : Es en los servicios donde recae todo el peso de la lógica de negocio. El servicio es el encargado de validar la entrada con respecto a las reglas del dominio, realizar las operaciones de acceso a datos y , en caso de ser necesario, devolver la información solicitada. En este proyecto puede parecer que los servicios son métodos de un modelo, que hemos desplazado y colocado en otro lugar, pero en realidad, un servicio no tiene por que estar asociado a un único modelo, es más, en aplicaciones donde se combinan varios modelos diferentes para dar un servicio determinado, ésta capa de servicios puede estar dentro de una aplicación que no tiene modelos propios (por ejemplo imaginemos una aplicación *dashboard* que muestra info de todas las aplicaciones, esta aplicación no tendría modelos propios pero si servicios.) . Además esta capa de servicios es la que, en principio, puede tener acceso a otros servicios de aplicaciones funcionando como un "puerto" de conexión entre las apps del proyecto. Los servicios deben ser lo más atómicos y ortogonales posibles para poder combinarse entre ellos.

##### Algunas Ventajas de esta arquitectura 

- Reducir al mínimo la responsabilidad de los serializadores, los formularios y los modelos , hace que escribir test para ellos sea casi innecesario ya que no se salen de la funcionalidad para la que fueron desarrollados (en la mayoria de los casos su funcionalidad queda probada al probar las vistas o las apis)
- El uso de servicios en aplicaciones separadas de las capas de presentación o de las tareas programadas, nos permite tener aplicaciones más pequeñas y manejables con pocos  archivos y reducir el acoplamiento a diferentes frameworks o herramientas (Django rest framework, Celery ...)
- Al unificar la lógica en los servicios e independizar sus dependencias podemos reutilizarlos en diferentes lugares sin añadir complejidad al sistema o tener que volver a desarrollar test. 
- Las limitaciones en el uso de serializadores evita que se reutilicen de forma errónea o innecesaria. 
- Es más fácil e intuitivo saber el lugar donde colocar un nuevo elemento. 
- Eliminar funcionalidades innecesarias es menos complejo que en una arquitectura Django regular en proyectos grandes.



### Puesta en marcha 

##### Configurar variables de entorno 

lo primero que debemos hacer para poder arrancar la aplicación es configurar las variables de entorno. para ello debemos copiar el archivo */app/.env.orig* en un archivo .env y sustituir los valores de las variables de entorno definidas, por valores reales .

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

Para ello, con el contenedor corriendo, debemos ejecutar el siguiente comando en la consola del anfitrión.

```bash
docker exec -i tasks_manager_web_1 python manage.py shell < scripts/init_data.py
```

Éste script creará un usuario demo con acceso root y  tareas de prueba. 

*El nombre de usuario y la contraseña de acceso son demo:demo*



**Ejecutar los test**

El sistema dispone de unos 150 test que se ejecutan en aproximadamente 15s

```bash
docker exec -it tasks_manager_web_1 python manage.py test
```



##### Acceso a la interfaz web

El acceso a la interfaz web se realiza mediante http://localhost:9000  con el contenedor en ejecución. 



### Documentación de la API 

La documentación de la api  se encuentra en el archivo ***API_DOC.md*** de éste mismo proyecto y un conjunto de funciones python preparados para consumir dicha api pueden consultarse en *scripts/endpoints.py*



### Carencias y posibles mejoras 

- Todas las APIs comparten estructura similar, lo que podría unificarse en una clase base, haciendo así que los mensajes que se envian al usuario queden unificados 
- Las vistas tambien comparten la misma estructura por lo que se podría aplicar una solución similar a las de las apis 
- Se podrian internacionalizar tanto las vistas y apis como las plantillas para traducir los textos a diferentes idiomas. 
- Las imágenes pueden comprimirse al subirse a AWS para evitar malgastar almacenamiento y reducir costes 
- Todas las respuetas de errores tienen la misma estructura por lo que podrían refactorizarse en su propia clase.
- Documentación de la API mediante alguna herramienta automática como SwaggerUI



#### Disclaimer y conclusiones finales

Utilizar este diseño personalizado tiene como objetivo demostrar mi forma de pensar al intentar abordar una solución intentando no solo resolver el problema en si sino que la solución sea mantenible y por lo tanto el coste de desarrollo para soluciones de igual complejidad, permanezca lo más constante posible. Esta arquitectura ha dado un muy buen resultado solucionando los problemas del proyecto en el que trabajo actualmente, pero no tiene por que ser una solución válida universalmente, hay ocasiones en las que seguir la estructura regular de un proyecto de Django, es la mejor opción, sobre todo en proyectos simples o cuya probabilidad de crecer y evolucionar sea pequeña.



#### Bibliografia y fuentes de insiparción 

E diseño de esta arquitectura es la combinación y recopilación de conocimientos de otros autores, Aunque las decisiones finales y el diseño han sido realizados para el proyecto en el que trabajo, no han sido desarrollados por mi desde 0 sino que me he inspirado en los siguientes recursos 

###### Guía de Estilos de Django desarrollada por HackSoftware

Es la principal inspiración de la arquitectura tomando bastantes elementos de lo que exponen y desechando muchos otros. Me ayudó a perfilar y mejorar el uso que ya hacía de los servicios. 

 https://github.com/HackSoftware/Django-Styleguide . 

###### Libros 

 *Código sostenible* (Carlos Blé Jurado) 

 *La artesanía del código limpio* - Robert C. Martin (libro)



