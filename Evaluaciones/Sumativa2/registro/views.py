from django.shortcuts import render, redirect
from django.urls import reverse
from inicio.models import Categoria,Caracteristica
import json

def espacios_vacios(value):
    return bool(value.strip()) 

def register(request):
    categorias = Categoria.objects.all()
    listaCaracteristicas = Caracteristica.CARACTERISTICAS

    listaCaracteristicas_json = json.dumps(listaCaracteristicas)
    
    return render(request, 'registro.html', {
        'listaCaracteristicas': listaCaracteristicas,
        'listaCaracteristicas_json': listaCaracteristicas_json,
        'categorias': categorias,
    })

def registrado(request):
    if request.method == "POST":
        codigo = request.POST.get('codigo')
        marca = request.POST.get('marca')
        nombre = request.POST.get('nombre')
        categoria = request.POST.get('categoria')
        
        caracteristicas_nombre = request.POST.getlist('caracteristicas_nombre')
        caracteristicas_detalle = request.POST.getlist('caracteristicas_detalle')

        # Comprobar si los campos están vacíos o solo contienen espacios
        code = espacios_vacios(codigo)
        name = espacios_vacios(nombre)
        mark = espacios_vacios(marca)
        category = espacios_vacios(categoria)
        
        for nombre, detalle in zip(caracteristicas_nombre, caracteristicas_detalle):
            print(f'Nombre: {nombre}, Detalle: {detalle}')

        if not (code and name and mark and category) or not codigo.startswith("#") or category == None:
            error_message = "Todos los campos son obligatorios y no pueden estar vacíos o solo contener espacios, ademas el codigo empiece con # y la fecha un formato valido"
            return render(request, 'registro.html', context={'error_message': error_message})
        else:
            return redirect(reverse('validacion', kwargs={
                'codigo': codigo
            }))

    return redirect('register')
