<div align="center">
  PROYECTO DJANGO PRODUCTORASA
</div>


REQUISITOS:
-----

Antes de comenzar debe instalar python en su computadora, para ello dirijase a la pagina oficial [PYTHON](https://www.python.org/downloads/) luego de haber seguido los pasos de la instalacion para python necesita en su sistema instalar git, hagalo mediante el siguiente enlace [GIT](https://git-scm.com/download/), aqui escoja el sistema operativo correspondiente a su PC.

Para poder ejecutar el proyecto de django debe tambien tener Visual Studio Code mediante el siguiente enlace [VSCode](https://code.visualstudio.com/download), aqui tambien debe escoger segun el sistema operativo que este utilizando actualmente,
habiendo terminado la instalacion, abra Visual Studio Code y dirijase a la ventana lateral de extensiones, esta tiene forma de
cuatro cuadrados, alli escriba 'python' e instale la extension, al finalizar abra una terminal con 'CTRL + Ñ' y escriba dentro de
ella '**pip install django**' y presione Enter. Si no puede realizar el comando reinicie la aplicacion de VSCode.

Ahora copie el siguiente link '**https://github.com/JaimeBustos2000/Programacion-BackEnd.git**', abra denuevo la terminal y escriba **'git clone'** y copie el link con CTRL+V, luego dele a Enter. Ahora vaya a 'Archivo', 'Abrir carpeta' y seleccione sumativa1. Si observa en la carpeta actual vera un archivo que se llama manage.py, este archivo maneja el control de la aplicacion principal y permite su ejecucion.

APLICACION WEB:
-----
Esta aplicacion se genera por medio del framework de backend DJANGO de python esta se subdivide en carpetas en formato de modulos que representaran cada uno de las paginas visibles, el inicio, el registro de productos, la lista de productos, etc, ademas constara con modulos reutilizables mediante los templates de django sumando tambien los elementos esteticos por medio de CSS.

...
Para esta ocasion, se han dispuesto la utilizacion de modelos para crear las tablas e interaccion con la base de datos por medio de sqlite3, dejando al framework la tarea de administrador de los datos.

Si desea iniciar la aplicacion web basta con escribir el siguiente comando en la terminal de vscode '**python manage.py runserver**' y presionar Enter, esto iniciara el proceso de la app web, el cual le enviara un mensaje en la terminal con un link del siguiente estilo '**http://127.0.0.1:8000/**', copie este enlace en su navegador y vera que la aplicacion estara operativa.

Ante cualquier error de ejecucion