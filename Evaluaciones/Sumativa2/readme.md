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
Si desea iniciar la aplicacion web basta con escribir el siguiente comando en la terminal de vscode '**python manage.py runserver**' y presionar Enter, esto iniciara el proceso de la app web, el cual le enviara un mensaje en la terminal con un link del siguiente estilo '**http://127.0.0.1:8000/**', copie este enlace en su navegador y vera que la aplicacion estara operativa. Revise que la carpeta donde se encuentra es la que contiene el archivo 'manage.py', si no es el caso abra la carpeta correcta en la parte superior de VsCode.

USO DE APLICACION:
-----
Para utilizar la aplicacion correctamente tenga en cuenta lo siguiente:

     1) Respetar el tipo de campo. Los campos que requieren un tipo de dato especifico tienen una pista de llenado.

     2) Al añadir nuevas marcas, nombre caracteristicas y categoria, verifique que estas hayan sido añadidas correctamente 
     revisando si en el campo del formulario de registro esta presente el atributo añadido.

     3) Solo puede añadir productos que tengan un nombre unico, codigo unico y que los campos no contengan solo espacios ya 
     que dara error.

     4) Todos los errores se mostraran en una alerta emergente.

     5) Puede acceder a la pagina de administracion de django para editar en profundidad las marcas, caracteristicas y 
     categorias tiene el siguiente link '**http://127.0.0.1:8000/admin**'

     6) Para ingresar debe utilizar el usuario: admin  y la contraseña: inacap2024

     7) Hay una tabla intermedia para añadir el texto en cada caso es: opcioncaracteristica, opcioncategoria y 
     nombremarca, aqui solo se asocian los nombres el cual puede ser cualquiera que se desee, para añadir 
     correctamente cada uno de los campos debe luego agregarlo en las tablas caracteristica, categoria o marca 
     respectivamente.

    REGISTROS:
    
    Detalles adicionales acerca del llenado de registros:

     1) El programa permite añadir productos sin caracteristicas o con multiples de estas.

     2) Luego de añadir un producto vera una pantalla con el detalle del producto añadido.
