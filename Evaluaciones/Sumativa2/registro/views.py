from django.shortcuts import render, redirect
from django.urls import reverse
from inicio.models import Categoria,OpcionCaracterisca,Marca,NombreMarca,Caracteristica,Producto,OpcionCategoria
import json
import time
from django.db import IntegrityError

def espacios_vacios(value):
    return bool(value.strip()) 

def validacion(*args):
    for elem in args:
        if elem == False:
            return False
    return True

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

def registrado(request):
    if request.method == "POST":
        codigo = request.POST.get('codigo')
        marca = request.POST.get('marca')
        nombre = request.POST.get('nombre')
        categoria = request.POST.get('categoria')
        
        objeto_marca = NombreMarca.objects.filter(nombre=marca).first().id
        marca_producto = Marca.objects.filter(nombre=objeto_marca)

        print("codigo: ", codigo)
        print("Marca: ", objeto_marca)
            
        """objeto_categoria = Categoria.objects.get(nombre=categoria)
        caracteristicas_nombre = request.POST.getlist('caracteristicas_nombre[]')
        caracteristicas_detalle = request.POST.getlist('caracteristicas_detalle[]')

        # Comprobar si los campos están vacíos o solo contienen espacios
        code = espacios_vacios(codigo)
        name = espacios_vacios(nombre)
        mark = espacios_vacios(marca)
        category = espacios_vacios(categoria)
        
        campos_validos = validacion(code, name, mark, category)
        listas_validas = bool(caracteristicas_detalle) and bool(caracteristicas_nombre)
        
        print("Listas validas: ", listas_validas)
        print("Campos validos: ", campos_validos)
        
        if campos_validos and listas_validas:
            producto = Producto.objects.create(codigo=codigo, marca=objeto_marca, nombre=nombre, categoria=objeto_categoria)
            
            for nombre, detalle in zip(caracteristicas_nombre, caracteristicas_detalle):
                print(f'Nombre: {nombre}, Detalle: {detalle}')
                
                # Crear la característica
                opcion_caracteristica = OpcionCaracterisca.objects.get(nombre=nombre)
                caracteristica = Caracteristica.objects.create(nombre=opcion_caracteristica, descripcion=detalle)
                
                # Asociar la característica con el producto
                producto.caracteristicas.add(caracteristica)
                
            producto.save()
            return redirect(reverse('validacion', kwargs={
                'codigo': codigo
            }))
        elif campos_validos and listas_validas==False:
            producto = Producto.objects.create(codigo=codigo, marca=objeto_marca, nombre=nombre, categoria=objeto_categoria)
            producto.save()
            return redirect(reverse('validacion', kwargs={
                'codigo': codigo
            }))
        else:
            error_message = "Hay errores en los campos, verifique los datos ingresados"
            return render(request, 'registro.html', context={'error_message': error_message})"""
        
        return redirect(reverse('validacion', kwargs={
                    'codigo': codigo
                }))

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

def nuevaCategoria(request):
    categorias = Categoria.objects.all()
    listaCaracteristicas = OpcionCaracterisca.objects.all().order_by('nombre')
    lista_caracteristicas_json = json.dumps([str(caracteristica) for caracteristica in listaCaracteristicas])
    
    marcas = Marca.objects.all()
    
    if request.method == "POST":
        categoria = request.POST.get('categoria')
        
        if espacios_vacios(categoria):
            nombre_categoria = OpcionCategoria.objects.create(nombre=categoria)
            Categoria.objects.create(nombre=nombre_categoria)
            
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

def nuevaCaracteristica(request):
    categorias = Categoria.objects.all()
    listaCaracteristicas = OpcionCaracterisca.objects.all().order_by('nombre')
    lista_caracteristicas_json = json.dumps([str(caracteristica) for caracteristica in listaCaracteristicas])
    
    marcas = Marca.objects.all()
    if request.method == "POST":
        caracteristica = request.POST.get('caracteristica')
        
        if espacios_vacios(caracteristica):
            OpcionCaracterisca.objects.create(nombre=caracteristica)
            
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