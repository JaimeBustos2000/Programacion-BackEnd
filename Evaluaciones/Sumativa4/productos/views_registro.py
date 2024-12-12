from django.shortcuts import render, redirect
from django.urls import reverse
from inicio.models import Categoria,Marca,Caracteristica,Producto,NombreCaracteristica
import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError
import requests



############# Visor de grupo ##################
def is_in_group(group_name):
    def check(user):
        return user.groups.filter(name=group_name).exists()
    return check

def is_in_group_any(user):
    # Verifica si el usuario pertenece a uno de los grupos
    return user.groups.filter(name__in=['admin_products', 'general']).exists()
###############################################


# Verificar que los campos no tengan solo espacios
def espacios_vacios(value):
    return bool(value.strip())

# Metodo para iterar sobre una lista de campos y verificar si todos son True(No vacios)
def validacion(*args):
    for elem in args:
        if elem == False:
            return False
    return True

# Vista de inicio del formulario
@user_passes_test(is_in_group("admin_products"),login_url='main')
@login_required
def register_page(request):
    mensaje = request.GET.get("mensaje",'')
    categorias = Categoria.objects.all()
    listaCaracteristicas = NombreCaracteristica.objects.all().order_by('nombre')
    lista_caracteristicas_json = json.dumps([str(caracteristica) for caracteristica in listaCaracteristicas])
    marcas = Marca.objects.all()
    
    return render(request, 'registro.html', {
        'error_message': None,
        'listaCaracteristicas': listaCaracteristicas,
        'listaCaracteristicas_json': lista_caracteristicas_json,
        'categorias': categorias,
        'marcas': marcas,
        'mensaje':mensaje
    })

# Vista para validar el registro de un producto
@user_passes_test(is_in_group('admin_products'),login_url='main')
@login_required
def nuevo_producto(request):
    if request.method == "POST":
        # Datos unicos
        codigo = request.POST.get('codigo')
        id_marca = int(request.POST.get('marca'))
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        id_categoria = int(request.POST.get('categoria'))
        
        copia_post = request.POST.copy()
            
        code = espacios_vacios(codigo)
        name = espacios_vacios(nombre)
        
        categorias = Categoria.objects.all()
        listaCaracteristicas = NombreCaracteristica.objects.all().order_by('nombre')
        lista_caracteristicas_json = json.dumps([str(caracteristica) for caracteristica in listaCaracteristicas])
        marcas = Marca.objects.all()
        
        if len(codigo) < 6 or ' ' in codigo:
            return render(request, 'registro.html', 
                          context={'error_message': "El código debe tener al menos 6 caracteres sin espacios", 
                                    'categorias': categorias, 
                                    'marcas': marcas, 
                                    'listaCaracteristicas': listaCaracteristicas, 
                                    'listaCaracteristicas_json': lista_caracteristicas_json})
        
        # Transformar precio a entero
        try:
            precio = int(precio)
        except ValueError as e:
            error_message = "El precio debe ser un número entero"
            
            return render(request, 'registro.html', context={
                'mensaje': None,
                'error_message': error_message, 
                'categorias': categorias, 
                'marcas': marcas, 
                'listaCaracteristicas': listaCaracteristicas, 
                'listaCaracteristicas_json': lista_caracteristicas_json})
        
        # Respuesta api
        api_url = "http://127.0.0.1:8000/productos/api/addproducto/"
        
        # Obtener la marca y la categoria
        marca = Marca.objects.get(id=id_marca)
        
        categoria = Categoria.objects.get(id=id_categoria)
        
        # Obtener la lista de caracteristicas con detalles
        caracteristicas_nombre = request.POST.getlist('caracteristicas_nombre[]')
        caracteristicas_detalle = request.POST.getlist('caracteristicas_detalle[]')

        # Comprobar si los campos están vacíos o solo contienen espacios

        
        # Comprobar si las listas de caracteristicas y detalles no están vacías
        campos_validos = validacion(code, name)
        listas_validas = bool(caracteristicas_detalle) and bool(caracteristicas_nombre)
        
        # Crear el producto con las caracteristicas
        if campos_validos and listas_validas:
            caracteristicas_list = []
            for nombre, detalle in zip(caracteristicas_nombre, caracteristicas_detalle):
                caracteristicas_list.append({
                    "nombre": nombre,
                    "detalle": detalle
                })
                
            api_caracteristicas = "http://127.0.0.1:8000/productos/api/addcaracteristicas/"
            payload_caracteristicas = { caracteristicas_list }
            response_caracteristicas = requests.post(api_caracteristicas, json=payload_caracteristicas)
            print(response_caracteristicas.status_code)
            if response_caracteristicas.status_code == 200 or response_caracteristicas.status_code == 201:
                data = response_caracteristicas.json()
                caracteristicas_ids = data.get('id')
                copia_post['caracteristicas'] = caracteristicas_ids
            else:
                error_message = "Error al crear las caracteristicas"
                return render(request, 'registro.html', {
                    'mensaje': None,
                    'error_message': error_message,
                    'listaCaracteristicas': listaCaracteristicas,
                    'listaCaracteristicas_json': lista_caracteristicas_json,
                    'categorias': categorias,
                    'marcas': marcas,
                })
            
            del copia_post['csrfmiddlewaretoken']
            del copia_post['caracteristicas_nombre[]']
            del copia_post['caracteristicas_detalle[]']
            print(copia_post)
            
            payload = copia_post
            
            response = requests.post(api_url, json=payload)
            print(response.status_code)
            if response.status_code == 200 or response.status_code == 201:
                mensaje = "Producto añadido correctamente"
                data = response.json()
                product_id = data.get('id')
                return redirect(f"{reverse('validacion')}?mensaje={mensaje}&id={product_id}")
            else:
                error_message = "Error al crear el producto."
                return render(request, 'registro.html', {
                    'mensaje': None,
                    'error_message': error_message,
                    'listaCaracteristicas': listaCaracteristicas,
                    'listaCaracteristicas_json': lista_caracteristicas_json,
                    'categorias': categorias,
                    'marcas': marcas,
                })
            
        elif campos_validos and listas_validas == False:
            # Crear el producto si no hay caracteristicas
            copia_post = copia_post.dict()
            del copia_post['csrfmiddlewaretoken']
            del copia_post['caracteristicas_nombre[]']
            del copia_post['caracteristicas_detalle[]']
            payload = copia_post
            
            response = requests.post(api_url, json=payload)
            if response.status_code == 200 or response.status_code == 201:
                mensaje = "Producto añadido correctamente"
                data = response.json()
                product_id = data.get('id')
                return redirect(f"{reverse('validacion')}?mensaje={mensaje}&id={product_id}")
            else:
                error_message = "Error al crear el producto."
                return render(request, 'registro.html', {
                    'mensaje': None,
                    'error_message': error_message,
                    'listaCaracteristicas': listaCaracteristicas,
                    'listaCaracteristicas_json': lista_caracteristicas_json,
                    'categorias': categorias,
                    'marcas': marcas,
                })
        
        else:
            error_message = "Hay errores en los campos, verifique los datos ingresados"
            return render(request, 'registro.html', context={'error_message': error_message})
        
    return redirect(reverse('validacion', kwargs={
                    'codigo': codigo
                }))

@user_passes_test(is_in_group, login_url='main')
@login_required
def nuevaMarca(request):
    if request.method == "POST":
        marca = request.POST.get('marca')
        categorias = Categoria.objects.all()
        listaCaracteristicas = NombreCaracteristica.objects.all().order_by('nombre')
        lista_caracteristicas_json = json.dumps([str(caracteristica) for caracteristica in listaCaracteristicas])
        marcas = Marca.objects.all()
        
        if marca and not marca.isspace() and espacios_vacios(marca):
            api_url = "http://127.0.0.1:8000/productos/api/addmarca/"
            payload = {"nombre": marca}
            response = requests.post(api_url, json=payload)

            if response.status_code == 200 or response.status_code == 201:
                mensaje = "Añadida nueva marca"
                # Redirigir con el mensaje como parámetro en la URL
                return redirect(f"{reverse('register_page')}?mensaje={mensaje}")
            else:
                error_message = "Error al crear la marca."
                return render(request, 'registro.html', {
                    'mensaje': None,
                    'error_message': error_message,
                    'listaCaracteristicas': listaCaracteristicas,
                    'listaCaracteristicas_json': lista_caracteristicas_json,
                    'categorias': categorias,
                    'marcas': marcas,
                })
        else:
            
            error_message = "El campo no puede estar vacío o solo contener espacios."
            return render(request, 'registro.html', {
                'mensaje': None,
                'error_message': error_message,
                'listaCaracteristicas': listaCaracteristicas,
                'listaCaracteristicas_json': lista_caracteristicas_json,
                'categorias': categorias,
                'marcas': marcas,
            })

    return render(request, 'registro.html', {
        'mensaje': "Ingreso no permitido",
        'listaCaracteristicas': listaCaracteristicas,
        'listaCaracteristicas_json': lista_caracteristicas_json,
        'categorias': categorias,
        'marcas': marcas,
    })


@user_passes_test(is_in_group('admin_products'),login_url='main')
@login_required
def nuevaCategoria(request):    
    if request.method == "POST":
        categoria = request.POST.get('categoria')
        categorias = Categoria.objects.all()
        listaCaracteristicas = NombreCaracteristica.objects.all().order_by('nombre')
        lista_caracteristicas_json = json.dumps([str(caracteristica) for caracteristica in listaCaracteristicas])
        marcas = Marca.objects.all()
        
        if categoria and not categoria.isspace() and espacios_vacios(categoria):
            api_url = "http://127.0.0.1:8000/productos/api/addcategoria/"
            payload = {"nombre": categoria}
            response = requests.post(api_url, json=payload)
            print(response.status_code)
            if response.status_code == 200 or response.status_code == 201:
                mensaje = "Añadida nueva categoría"
                # Redirigir con el mensaje como parámetro en la URL
                return redirect(f"{reverse('register_page')}?mensaje={mensaje}")
            else:
                error_message = "Error al crear la categoría."
                return render(request, 'registro.html', {
                    'mensaje': None,
                    'error_message': error_message,
                    'listaCaracteristicas': listaCaracteristicas,
                    'listaCaracteristicas_json': lista_caracteristicas_json,
                    'categorias': categorias,
                    'marcas': marcas,
                })
                
        else:
            error_message = "El campo no puede estar vacío o solo contener espacios"
            return render(request, 'registro.html', context={'error_message': error_message})
        
    return render(request, 'registro.html',{
                'mensaje': None,
                'listaCaracteristicas': listaCaracteristicas,
                'listaCaracteristicas_json': lista_caracteristicas_json,
                'categorias': categorias,
                'marcas': marcas})

@user_passes_test(is_in_group('admin_products'),login_url='main')
@login_required
def nuevaCaracteristica(request):
    if request.method == "POST":
        caracteristica = request.POST.get('caracteristica')
        categorias = Categoria.objects.all()
        listaCaracteristicas = NombreCaracteristica.objects.all().order_by('nombre')
        lista_caracteristicas_json = json.dumps([str(caracteristica) for caracteristica in listaCaracteristicas])
        marcas = Marca.objects.all()
        
        if caracteristica and not caracteristica.isspace() and espacios_vacios(caracteristica):
            api_url = "http://127.0.0.1:8000/productos/api/addcaracteristica/"
            payload = {"nombre": caracteristica}
            response = requests.post(api_url, json=payload)
            if response.status_code == 200 or response.status_code == 201:
                mensaje = "Añadida nueva característica"
                # Redirigir con el mensaje como parámetro en la URL
                return redirect(f"{reverse('register_page')}?mensaje={mensaje}")
            else:
                error_message = "Error al crear la característica."
                return render(request, 'registro.html', {
                    'mensaje': None,
                    'error_message': error_message,
                    'listaCaracteristicas': listaCaracteristicas,
                    'listaCaracteristicas_json': lista_caracteristicas_json,
                    'categorias': categorias,
                    'marcas': marcas,
                })
        else:
            error_message = "El campo no puede estar vacío o solo contener espacios"
            return render(request, 'registro.html', context={'error_message': error_message})
        
    return render(request,'register_page',{
                'mensaje': None,
                'listaCaracteristicas': listaCaracteristicas,
                'listaCaracteristicas_json': lista_caracteristicas_json,
                'categorias': categorias,
                'marcas': marcas})