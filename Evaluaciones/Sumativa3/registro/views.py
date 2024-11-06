from django.shortcuts import render, redirect
from django.urls import reverse
from inicio.models import Categoria,OpcionCaracterisca,Marca,NombreMarca,Caracteristica,Producto,OpcionCategoria
import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError

############# Visor de grupo ##################
def is_in_group(group_name):
    def check(user):
        return user.groups.filter(name=group_name).exists()
    return check

def is_in_group_any(user):
    # Verifica si el usuario pertenece a uno de los grupos
    return user.groups.filter(name__in=['admin_products', 'general']).exists()
############# Visor de grupo ##################


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
@login_required
def register(request):
    categorias = Categoria.objects.all()
    listaCaracteristicas = OpcionCaracterisca.objects.all().order_by('nombre')
    lista_caracteristicas_json = json.dumps([str(caracteristica) for caracteristica in listaCaracteristicas])
    
    marcas = Marca.objects.all()
    
    return render(request, 'registro.html', {
        'listaCaracteristicas': listaCaracteristicas,
        'listaCaracteristicas_json': lista_caracteristicas_json,
        'categorias': categorias,
        'marcas': marcas
    })

# Vista para validar el registro de un producto
@user_passes_test(is_in_group('admin_products'),login_url='main')
@login_required
def registrado(request):
    if request.method == "POST":
        # Cargar datos de la base de datos
        categorias = Categoria.objects.all()
        listaCaracteristicas = OpcionCaracterisca.objects.all().order_by('nombre')
        lista_caracteristicas_json = json.dumps([str(caracteristica) for caracteristica in listaCaracteristicas])
        marcas = Marca.objects.all()
        
        # Datos unicos
        codigo = request.POST.get('codigo')
        id_marca = int(request.POST.get('marca'))
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        id_categoria = int(request.POST.get('categoria'))
        
        code = espacios_vacios(codigo)
        print(code)
        name = espacios_vacios(nombre)
        
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
                'error_message': error_message, 
                'categorias': categorias, 
                'marcas': marcas, 
                'listaCaracteristicas': listaCaracteristicas, 
                'listaCaracteristicas_json': lista_caracteristicas_json})
        
        # Comprobar si el código ya existe
        if Producto.objects.filter(codigo=codigo).exists():
            error_message = "El código ya existe"
            return render(request, 'registro.html', context={'error_message': error_message, 
                                                             'categorias': categorias, 
                                                             'marcas': marcas, 
                                                             'listaCaracteristicas': listaCaracteristicas, 
                                                             'listaCaracteristicas_json': lista_caracteristicas_json})
        
        # Comprobar si el nombre ya existe
        if Producto.objects.filter(nombre=nombre).exists():
            error_message = "El nombre ya existe"
            return render(request, 'registro.html', context={'error_message': error_message, 
                                                             'categorias': categorias, 
                                                             'marcas': marcas, 
                                                             'listaCaracteristicas': listaCaracteristicas, 
                                                             'listaCaracteristicas_json': lista_caracteristicas_json})
        
        # Obtener la marca y la categoria
        opcion_marca = NombreMarca.objects.get(id=id_marca)
        marca = Marca.objects.get(nombre=opcion_marca)
        
        opcion_categoria = OpcionCategoria.objects.get(id=id_categoria)
        categoria = Categoria.objects.get(nombre=opcion_categoria)
        
        # Obtener la lista de caracteristicas con detalles
        caracteristicas_nombre = request.POST.getlist('caracteristicas_nombre[]')
        caracteristicas_detalle = request.POST.getlist('caracteristicas_detalle[]')

        # Comprobar si los campos están vacíos o solo contienen espacios

        
        # Comprobar si las listas de caracteristicas y detalles no están vacías
        campos_validos = validacion(code, name)
        listas_validas = bool(caracteristicas_detalle) and bool(caracteristicas_nombre)
        
        # Crear el producto con las caracteristicas
        if campos_validos and listas_validas:
            producto = Producto.objects.create(codigo=codigo, marca=marca, nombre=nombre, categoria=categoria,precio=precio)
            
            # Desempaquetar las listas de caracteristicas y detalles
            for nombre, detalle in zip(caracteristicas_nombre, caracteristicas_detalle):
                print(f'Nombre: {nombre}, Detalle: {detalle}')
                
                # Crear la característica
                opcion_caracteristica = OpcionCaracterisca.objects.get(nombre=nombre)
                caracteristica = Caracteristica.objects.create(nombre=opcion_caracteristica, descripcion=detalle)
                
                # Asociar la característica con el producto
                producto.caracteristicas.add(caracteristica)
            
            # Vericar que los campos del producto sean validos y guardarlo    
            producto.full_clean()    
            producto.save()
            return redirect(reverse('validacion', kwargs={
                'codigo': codigo
            }))
            
        elif campos_validos and listas_validas==False:
            # Crear el producto si no hay caracteristicas
            producto = Producto.objects.create(codigo=codigo, marca=id_marca,precio=precio, nombre=nombre, categoria=id_categoria)
            producto.full_clean() 
            producto.save()
            return redirect(reverse('validacion', kwargs={
                'codigo': codigo
            }))
        
        else:
            error_message = "Hay errores en los campos, verifique los datos ingresados"
            return render(request, 'registro.html', context={'error_message': error_message})
        
    return redirect(reverse('validacion', kwargs={
                    'codigo': codigo
                }))

@user_passes_test(is_in_group('admin_products'),login_url='main')
@login_required
def nuevaMarca(request):
    categorias = Categoria.objects.all()
    listaCaracteristicas = OpcionCaracterisca.objects.all().order_by('nombre')
    lista_caracteristicas_json = json.dumps([str(caracteristica) for caracteristica in listaCaracteristicas])
    marcas = Marca.objects.all()
    
    if request.method == "POST":
        marca = request.POST.get('marca')
        print(marca)
        
        if espacios_vacios(marca):
            try:
                nombre_marca=NombreMarca.objects.create(nombre=marca)
                Marca.objects.create(nombre=nombre_marca)
                marcas = Marca.objects.all()
            except IntegrityError as e:
                error_message = "La marca ya existe"
                return render(request, 'registro.html', 
                              context={
                                  'error_message': error_message, 
                                  'categorias': categorias, 
                                  'marcas': marcas, 
                                  'listaCaracteristicas': listaCaracteristicas, 
                                  'listaCaracteristicas_json': lista_caracteristicas_json})
                
            return render(request, 'registro.html',{
                'listaCaracteristicas': listaCaracteristicas,
                'listaCaracteristicas_json': lista_caracteristicas_json,
                'categorias': categorias,
                'marcas': marcas})
        else:
            error_message = "El campo no puede estar vacío o solo contener espacios"
            return render(request, 'registro.html', context={'error_message': error_message})
        
    return render(request,'register',{
                'listaCaracteristicas': listaCaracteristicas,
                'listaCaracteristicas_json': lista_caracteristicas_json,
                'categorias': categorias,
                'marcas': marcas})

@user_passes_test(is_in_group('admin_products'),login_url='main')
@login_required
def nuevaCategoria(request):    
    marcas = Marca.objects.all()
    listaCaracteristicas = OpcionCaracterisca.objects.all().order_by('nombre')
    lista_caracteristicas_json = json.dumps([str(caracteristica) for caracteristica in listaCaracteristicas])
    categorias = Categoria.objects.all()
    
    if request.method == "POST":
        categoria = request.POST.get('categoria')
        
        if espacios_vacios(categoria):
            try:
                nombre_categoria = OpcionCategoria.objects.create(nombre=categoria)
                Categoria.objects.create(nombre=nombre_categoria)
                categorias = Categoria.objects.all()

            except IntegrityError as e:
                error_message = "La categoria ya existe"
                return render(request, 'registro.html', 
                              context={
                                  'error_message': error_message, 
                                  'categorias': categorias, 
                                  'marcas': marcas, 
                                  'listaCaracteristicas': listaCaracteristicas, 
                                  'listaCaracteristicas_json': lista_caracteristicas_json})

            return render(request, 'registro.html',{
                'listaCaracteristicas': listaCaracteristicas,
                'listaCaracteristicas_json': lista_caracteristicas_json,
                'categorias': categorias,
                'marcas': marcas})
        else:
            error_message = "El campo no puede estar vacío o solo contener espacios"
            return render(request, 'registro.html', context={'error_message': error_message})
        
    return render(request, 'registro.html',{
                'listaCaracteristicas': listaCaracteristicas,
                'listaCaracteristicas_json': lista_caracteristicas_json,
                'categorias': categorias,
                'marcas': marcas})

@user_passes_test(is_in_group('admin_products'),login_url='main')
@login_required
def nuevaCaracteristica(request):
    marcas = Marca.objects.all()
    categorias = Categoria.objects.all()
    listaCaracteristicas = OpcionCaracterisca.objects.all().order_by('nombre')
    lista_caracteristicas_json = json.dumps([str(caracteristica) for caracteristica in listaCaracteristicas])
    
    if request.method == "POST":
        caracteristica = request.POST.get('caracteristica')
        
        if espacios_vacios(caracteristica):
            try:
                OpcionCaracterisca.objects.create(nombre=caracteristica)
                listaCaracteristicas = OpcionCaracterisca.objects.all().order_by('nombre')
                lista_caracteristicas_json = json.dumps([str(caracteristica) for caracteristica in listaCaracteristicas])
            except IntegrityError as e:
                error_message = "La caracteristica ya existe"
                return render(request, 'registro.html', 
                              context={
                                  'error_message': error_message, 
                                  'categorias': categorias, 
                                  'marcas': marcas, 
                                  'listaCaracteristicas': listaCaracteristicas, 
                                  'listaCaracteristicas_json': lista_caracteristicas_json})
            
            return render(request,'registro.html',{
                'listaCaracteristicas': listaCaracteristicas,
                'listaCaracteristicas_json': lista_caracteristicas_json,
                'categorias': categorias,
                'marcas': marcas})
        else:
            error_message = "El campo no puede estar vacío o solo contener espacios"
            return render(request, 'registro.html', context={'error_message': error_message})
        
    return render(request,'register',{
                'listaCaracteristicas': listaCaracteristicas,
                'listaCaracteristicas_json': lista_caracteristicas_json,
                'categorias': categorias,
                'marcas': marcas})