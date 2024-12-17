<div align="center">
  <h1>PROYECTO DJANGO PRODUCTORASA</h1>
</div>

## Contenidos
- [Requisitos](#requisitos)
- [Clonar el Repositorio del Proyecto](#clonar-el-repositorio-del-proyecto)
- [Aplicación Web](#aplicacion-web)
- [Importante](#importante)
  - [Vistas de las App](#vistas-de-las-app)
  - [Medidas de Seguridad Aplicadas](#medidas-de-seguridad-aplicadas)
  - [Uso de Aplicación Administración de Productos](#uso-de-aplicacion-administracion-de-productos)
- [Registro de Productos Nuevos](#registro-de-productos-nuevos)
- [API](#api)

## Requisitos

Antes de comenzar debe instalar Python en su computadora. Para ello, diríjase a la página oficial [PYTHON](https://www.python.org/downloads/). Luego de seguir los pasos de la instalación para Python, necesita instalar Git en su sistema. Hágalo mediante el siguiente enlace [GIT](https://git-scm.com/download/), elija el sistema operativo correspondiente a su PC.

Para poder ejecutar el proyecto de Django, también debe tener Visual Studio Code mediante el siguiente enlace [VSCode](https://code.visualstudio.com/download), elija el sistema operativo que esté utilizando actualmente. Habiendo terminado la instalación, abra Visual Studio Code y diríjase a la ventana lateral de extensiones (tiene forma de cuatro cuadrados). Escriba 'python' e instale la extensión. Al finalizar, abra una terminal con `CTRL + Ñ` y escriba dentro de ella los siguientes comandos:

- `pip install django` y presione Enter.
  Si no puede realizar el comando, reinicie la aplicación de VSCode.
- Realice la misma operación con el comando `pip install django-cors-headers`.

## Clonar el Repositorio del Proyecto

Ahora copie el siguiente link `https://github.com/JaimeBustos2000/Programacion-BackEnd.git`, abra de nuevo la terminal y escriba `git clone` y pegue el link con `CTRL+V`, luego presione Enter. Ahora vaya a 'Archivo', 'Abrir carpeta' y seleccione `sumativa3`. Si observa en la carpeta actual, verá un archivo llamado `manage.py`. Este archivo maneja el control de la aplicación principal y permite su ejecución.

## Aplicación Web

Esta aplicación se genera por medio del framework de backend Django de Python. Está subdividida en carpetas en formato de módulos que representan cada una de las páginas visibles: el inicio, el registro de productos, la lista de productos, etc. Además, consta de módulos reutilizables mediante los templates de Django, sumando también los elementos estéticos por medio de CSS.

Para iniciar la aplicación web, basta con escribir el siguiente comando en la terminal de VSCode `python manage.py runserver` y presionar Enter. Esto iniciará el proceso de la aplicación web, el cual le enviará un mensaje en la terminal con un link del siguiente estilo `http://127.0.0.1:8000/`. Copie este enlace en su navegador y verá que la aplicación estará operativa. Revise que la carpeta donde se encuentra es la que contiene el archivo `manage.py`. Si no es el caso, abra la carpeta correcta en la parte superior de VSCode.

## Importante

### Vistas de las App

1. **INICIO**: Página principal, login, información de la sesión, registro de usuario.
2. **PRODUCTOS**: Visualización de los productos existentes y filtros.
3. **REGISTRO**: Añadir nuevos productos (la actualización/eliminación está disponible solo por Django admin).
4. **RESULTADO**: Vista de éxito en caso de que los campos ingresados del formulario de creación estén correctos, presentando la información ingresada previamente y de manera ordenada.

### Medidas de Seguridad Aplicadas

1. **CSRF TOKEN**: Se añade al envío de los formularios para que solo se lean formularios provenientes del servidor de Django.
2. **Protección de Cross-Site Scripting (XSS)**: Utilizando el sistema de formularios propios de Django, se envía desde el backend al frontend el formulario.
3. **Restricción de ingreso y acceso a vistas**: Solo usuarios autorizados por medio del módulo `django.contrib.auth`:
   - **Admin**: Permite todas las operaciones dentro de los modelos, acceso a Django admin, creación de grupos y usuarios, visualización y filtro de productos.
     - Usuario: admin, Contraseña: inacap2024
   - **admin_products**: Permite operaciones con los modelos existentes, acceso limitado a Django admin, creación de nuevos productos, características, categorías y marcas.
     - Usuario: franarias2550, Contraseña: inacap2024
   - **general**: Solo lectura de los productos actuales y filtros.
     - Usuario: usuario12345, Contraseña: inacap2024
   - `settings.py`:
     ```python
     LOGIN_URL="/"  # Redireccionamiento al inicio (login) cuando se intenta acceder a un dominio no autorizado.
     ```
4. **Uso de CORSHEADERS**: Limitación de dominios que pueden acceder a la web.
5. **Sesiones seguras**: Destrucción de sesiones al cerrar el navegador, limitación de cookies a https y sesiones en caché. Control de acceso mediante variables de sesión.
   ```python
   request.session['admin_products'] = user.groups.filter(name='admin_products').exists()

### Uso de aplicacion de administracion de productos:

Para utilizar la aplicación correctamente tenga en cuenta lo siguiente:

1. **Respetar el tipo de campo:** Los campos que requieren un tipo de dato específico tienen una pista de llenado.
2. **Añadir nuevas marcas, características y categorías:** Verifique que estas hayan sido añadidas correctamente revisando si en el campo del formulario de registro está presente en el atributo añadido.
3. **Unicidad de nombre y código:** Solo puede añadir productos que tengan un nombre único, código único y que los campos no contengan solo espacios, ya que esto generará un error.
4. **Errores:** Todos los errores se mostrarán en una alerta emergente.
5. **Acceder a la página de administración de Django:** Puede acceder a la página de administración de Django para editar en profundidad las marcas, características y categorías. Tiene el siguiente enlace: 
   - '**http://127.0.0.1:8000/admin**'
6. **Usuario de administración de Django:** 
   - Usuario: admin  
   - Contraseña: inacap2024
7. **Tabla intermedia:** Existe una tabla intermedia para añadir el texto en cada caso: `opcioncaracteristica`, `opcioncategoria` y `nombremarca`. Aquí solo se asocian los nombres, los cuales pueden ser cualquiera que desee. Para añadir correctamente cada uno de los campos, debe luego agregarlos en las tablas `caracteristica`, `categoria` o `marca`, respectivamente.

## REGISTRO DE PRODUCTOS NUEVOS:
-----

Detalles adicionales acerca del llenado de registros:

1. El programa permite añadir productos sin características o con múltiples de estas.
2. Después de añadir un producto, verá una pantalla con el detalle del producto añadido.

## API:
-----

Aquí se detalla cómo usar la API. Para acceder, en este caso está sin JWT, por lo que puede entrar a 'http://127.0.0.1:8000/productos/api/docs' sin requerir autorización de la sesión del usuario.

En este caso, las APIs se detallarán por orden de inserción y visualización en la página:

### AUTH:
1. **/token:** Esta API requiere un usuario y contraseña validados en el sistema que estén dentro del grupo `admin_products`, que son los que pueden administrar esto. *(No implementado)*

### ALL:
1. **/all:** Esta API obtiene todos los productos de la base de datos, no pide ningún dato para ingresar, por tanto, es solo ejecutar la API en la página web. *(Implementado)*

### PRODUCTS:
1. **/products/{pid}:** Obtiene un producto específico, el único argumento que recibe es un entero que debe estar dentro del rango de la base de datos. Si no existe, lanzará una excepción de error 404. *(Implementado)*
2. **/delete/{pid}:** Al ingresar el argumento de un ID válido, provocará la eliminación de dicho producto en la base de datos. *(Implementado)*
3. **/edit/{pid}:** Reemplaza los datos existentes del producto con los datos nuevos. *(No implementado)*
4. **/addproducto:** Permite insertar un nuevo producto, teniendo en cuenta los siguientes argumentos:
    - `codigo`: string de 7 de longitud y que empieza con #
    - `marca_id`: integer
    - `nombre`: string
    - `precio`: int
    - `categoria_id`: int
    - `caracteristicas`: lista de características referenciadas por sus IDs, si es que aplica (por lo que puede estar vacío). *(En revisión pero implementado)*
