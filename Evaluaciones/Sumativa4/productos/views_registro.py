from django.shortcuts import render, redirect
from django.urls import reverse
from inicio.models import Categoria,Marca,Caracteristica,Producto,NombreCaracteristica
import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError
import requests
from urllib.parse import quote


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
    categorias = Categoria.objects.all().order_by('nombre')
    listaCaracteristicas = NombreCaracteristica.objects.all().order_by('nombre')
    lista_caracteristicas_json = json.dumps([str(caracteristica) for caracteristica in listaCaracteristicas])
    marcas = Marca.objects.all().order_by('nombre')
    
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
            
        code = espacios_vacios(codigo)
        name = espacios_vacios(nombre)
        
        categorias = Categoria.objects.all()
        listaCaracteristicas = NombreCaracteristica.objects.all().order_by('nombre')
        lista_caracteristicas_json = json.dumps([str(caracteristica) for caracteristica in listaCaracteristicas])
        marcas = Marca.objects.all()
        
        if len(codigo) < 6 or ' ' in codigo or not codigo.startswith('#'):
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
        
        # Api url
        api_url = "http://127.0.0.1:8000/productos/api/addproducto/"
        
        
        # Obtener la lista de caracteristicas con detalles
        caracteristicas_nombre = request.POST.getlist('caracteristicas_nombre[]')
        caracteristicas_detalle = request.POST.getlist('caracteristicas_detalle[]')
        
        # Comprobar si las listas de caracteristicas y detalles no están vacías
        campos_validos = validacion(code, name)
        listas_validas = bool(caracteristicas_detalle) and bool(caracteristicas_nombre)
        
        # Crear el producto con las caracteristicas
        if campos_validos and listas_validas:
            try:
                caracteristicas_list = [
                    {"nombre": nombre, "detalle": detalle}
                    for nombre, detalle in zip(caracteristicas_nombre, caracteristicas_detalle)
                ]
            except:
                caracteristicas_list = []

            # Crear las caracteristicas y retornar ids
            try:
                caracteristicas_ids = []
                for caracteristica in caracteristicas_list:
                    nombre_caracteristica = NombreCaracteristica.objects.filter(nombre=caracteristica['nombre']).first()
                    caracteristica = Caracteristica.objects.create(nombre=nombre_caracteristica, descripcion=caracteristica['detalle'])
                    caracteristicas_ids.append(caracteristica.id)
            except:
                caracteristicas_ids = []
            
            if caracteristicas_ids:
                payload = {
                           "codigo": codigo,
                           "marca_id": id_marca,
                           "nombre": nombre,
                           "precio": precio,
                           "categoria_id": id_categoria,
                            "caracteristicas": caracteristicas_ids
                           }
            else:
                payload = {
                           "codigo": codigo,
                           "marca_id": id_marca,
                           "nombre": nombre,
                           "precio": precio,
                           "categoria_id": id_categoria,
                           "caracteristicas": []
                           }
                
            print("payload", payload)
            
            jwt = request.session.get('token')
            headers = {
                'Authorization': f'Bearer {jwt}'}
            
            response = requests.post(api_url, json=payload, headers=headers)
            
            if response.status_code == 200 or response.status_code == 201:
                
                data = response.json()
                product_id = data.get('id')
                return redirect(f"{reverse('validacion', kwargs={'id': product_id})}")
            else:
                error_message = response.json().get('error')
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
            headers = {
                'Authorization': f'Bearer {request.session["token"]}'}
            
            payload = {
                "codigo": codigo,
                "marca_id": id_marca,
                "nombre": nombre,
                "precio": precio,
                "categoria_id": id_categoria,
                "caracteristicas": []
            }
            
            response = requests.post(api_url, json=payload, headers=headers)
            # print(response.status_code)
            if response.status_code == 200 or response.status_code == 201:
                data = response.json()
                product_id = data.get('id')
                print("Producto creado con id:", product_id)
                return redirect(f"{reverse('validacion', kwargs={'id': product_id})}")
            else:
                error_message = response.json().get('error')
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

# Vista para nueva marca
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
            headers = {
                'Authorization': f'Bearer {request.session["token"]}',
                'Content-Type': 'application/json'
                }
            payload = {"nombre": marca}
            response = requests.post(api_url, json=payload, headers=headers)

            if response.status_code == 200 or response.status_code == 201:
                mensaje = "Añadida nueva marca"
                # Redirigir con el mensaje como parámetro en la URL
                return redirect(f"{reverse('register_page')}?mensaje={mensaje}")
            else:
                error_message = response.json().get('error')
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

# Vista para nueva categoria
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
            headers ={ 'Authorization': f'Bearer {request.session["token"]}'}
            
            response = requests.post(api_url, json=payload, headers=headers)

            if response.status_code == 200 or response.status_code == 201:
                
                return redirect(f"{reverse('register_page')}")
            else:
                error_message = response.json().get('error')
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
            headers = {'Authorization': f'Bearer {request.session["token"]}'}
            response = requests.post(api_url, json=payload, headers=headers)
            if response.status_code == 200 or response.status_code == 201:
                mensaje = "Añadida nueva característica"
                # Redirigir con el mensaje como parámetro en la URL
                return redirect(f"{reverse('register_page')}?mensaje={mensaje}")
            else:
                error_message = response.json().get('error')
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