<div align="center">
  PROYECTO DJANGO PRODUCTORASA
</div>


REQUISITOS:
-----

Antes de comenzar debe instalar python en su computadora, para ello dirijase a la pagina oficial [PYTHON](https://www.python.org/downloads/) luego de haber seguido los pasos de la instalacion para python necesita en su sistema instalar git, hagalo mediante el siguiente enlace [GIT](https://git-scm.com/download/), aqui escoja el sistema operativo correspondiente a su PC.

Para poder ejecutar el proyecto de django debe tambien tener Visual Studio Code mediante el siguiente enlace [VSCode](https://code.visualstudio.com/download), aqui tambien debe escoger segun el sistema operativo que este utilizando actualmente,
habiendo terminado la instalacion, abra Visual Studio Code y dirijase a la ventana lateral de extensiones, esta tiene forma de
cuatro cuadrados, alli escriba 'python' e instale la extension, al finalizar abra una terminal con 'CTRL + Ñ' y escriba dentro de
ella los siguientes comandos:

  - '**pip install django**' y presione Enter. 
    Si no puede realizar el comando reinicie la aplicacion de VSCode.

  - Realice la misma operacion con el comando '**pip install django-cors-headers**'.

CLONAR EL REPOSITORIO DEL PROYECTO:
-----
Ahora copie el siguiente link '**https://github.com/JaimeBustos2000/Programacion-BackEnd.git**', abra denuevo la terminal y escriba **'git clone'** y copie el link con CTRL+V, luego dele a Enter. Ahora vaya a 'Archivo', 'Abrir carpeta' y seleccione sumativa3. Si observa en la carpeta actual vera un archivo que se llama manage.py, este archivo maneja el control de la aplicacion principal y permite su ejecucion.

APLICACION WEB:
------
Esta aplicacion se genera por medio del framework de backend DJANGO de python esta se subdivide en carpetas en formato de modulos que representaran cada uno de las paginas visibles, el inicio, el registro de productos, la lista de productos, etc, ademas constara con modulos reutilizables mediante los templates de django sumando tambien los elementos esteticos por medio de CSS.

...
Si desea iniciar la aplicacion web basta con escribir el siguiente comando en la terminal de vscode '**python manage.py runserver**' y presionar Enter, esto iniciara el proceso de la aplicacion web, el cual le enviara un mensaje en la terminal con un link del siguiente estilo '**http://127.0.0.1:8000/**', copie este enlace en su navegador y vera que la aplicacion estara operativa. Revise que la carpeta donde se encuentra es la que contiene el archivo 'manage.py', si no es el caso abra la carpeta correcta en la parte superior de VsCode.

<div style="font-size:25px;">
  IMPORTANTE
</div>

VISTAS DE LAS APP(carpetas):

-INICIO: Pagina principal, login, informacion de la sesion, registro usuario.
-PRODUCTOS: Visualizacion de los productos existentes y filtros.
-REGISTRO: Añadir nuevos productos (En este caso la actualizacion/eliminacion esta disponible solo por django admin)
-RESULTADO: Vista de exito en caso de que los campos ingresados del formulario de creacion esten correctos, presentando
            la informacion ingresada previamente y de manera ordenada.



MEDIDAS DE SEGURIDAD APLICADAS:

  1) Se añade CSRF TOKEN al envio de los formularios para que solo se lean formularios provenientes del servidor de django.

  2) Proteccion de Cross-Site Scripting (XSS), por medio de la utilizacion del sistema de formularios propios de django,
    se envia desde el backend al frontend el formulario.

  3) Se restringe el ingreso y acceso a vistas a solo usuarios autorizados por medio del modulo django.contrib.auth:

    A) Admin: Se le permite realizar todas las operaciones dentro de los modelos incluyendo el ingreso
      a django admin, creacion de grupos y usuarios. Ademas visualizar los productos actuales con metodos
      de filtro. Ya de por si contiene los permisos del grupo admin_products.

          Usuario: admin   contraseña: inacap2024

    B) admin_products: Se le permite realizar operaciones con los modelos existentes, tambien tiene acceso a django admin
      pero solo puede interactuar en la creacion de nuevos productos,caracteristicas, categorias y marcas. 
      Tambien tiene acceso a visualizar los productos actuales y filtrarlos.

          Usuario: franarias2550    contraseña: inacap2024

    C) general: Solo permite lectura de los productos actuales y ademas filtrarlos.

          Usuario: usuario12345    contraseña:inacap2024

    PD: Las vistas como el login y registro estan protegidas solo para usuarios no autenticados. Por defecto solo se pueden crear
    usuarios con rol 'general' a travez de la app web, sin embargo se pueden crear o manipular con el usuario admin en django admin.

    settings.py/
    ...
    LOGIN_URL="/"    #Redireccionamiento al inicio en este caso el login cuando se intenta acceder a un dominio no autorizado.
    ...

  4) Uso de CORSHEADERS: Limitacion de dominios que pueden acceder a la web.

  5) Las sesiones que se destruyen al cerrar el navegador, limitacion de cookies solo a https y sesion en cache.

     En relacion a esto el acceso sera controlado por las variables de sesion, con una clave 'admin_products', que sera un booleano que consulta a la base de datos y almacena si el usuario pertenece o no a ese grupo. Por tanto esta consulta se hara una unica vez mientras se haya iniciado sesion.

                                                                                    booleano que arroja
        acceso a sesion    nombre_grupo             consulta por medio del ORM     si pertenece al grupo
           |||||||||      ||||||||||||||          ||||||||||||||||||||||||||||||      |||||||
     EJ: request.session['admin_products'] = user.groups.filter(name='admin_products').exists()

    PD: Se añade un debug-log para monitorear los accesos y errores provenientes de la aplicacion.


En resumen a lo anterior el flujo es el siguiente:

-usuario admin: Acceso total. Tanto a administracion como vistas.

-usuario del grupo admin_products: Edicion de productos, caracteristicas,categorias y marcas. Con acceso al admin de django.
  Tambien tiene acceso total a las vistas relacionadas a la administracion de productos.

-usuario del grupo general: Solo tiene permisos de lectura de los productos por medio de la app web sin acceso a admin de django.
  (simula un usuario comun)


USO DE APLICACION ADMINISTRACION DE PRODUCTOS:
-----
Para utilizar la aplicacion correctamente tenga en cuenta lo siguiente:

 1) Respetar el tipo de campo. Los campos que requieren un tipo de dato especifico tienen una pista de llenado.
 2) Al añadir nuevas marcas, nombre caracteristicas y categoria, verifique que estas hayan sido añadidas correctamente revisando si en el campo del formulario de registro esta presente en el atributo añadido.
 3) Solo puede añadir productos que tengan un nombre unico, codigo unico y que los campos no contengan solo espacios ya que dara error.
 4) Todos los errores se mostraran en una alerta emergente.
 5) Puede acceder a la pagina de administracion de django para editar en profundidad las marcas, caracteristicas y categorias tiene el siguiente link '**http://127.0.0.1:8000/admin**'
 6) Para ingresar debe utilizar el usuario: admin  y la contraseña: inacap2024
 7) Hay una tabla intermedia para añadir el texto en cada caso es: opcioncaracteristica, opcioncategoria y nombremarca, aqui solo se asocian los nombres el cual puede ser cualquiera que se desee, para añadir correctamente cada uno de los campos debe luego agregarlo en las tablas caracteristica, categoria o marca respectivamente.


REGISTRO DE PRODUCTOS NUEVOS:

Detalles adicionales acerca del llenado de registros:
 1) El programa permite añadir productos sin caracteristicas o con multiples de estas.
 2) Luego de añadir un producto vera una pantalla con el detalle del producto añadido.
