from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse

def espacios_vacios(value):
    return bool(value.strip()) 

def register(request):
    return render(request, 'registro.html')

def registrado(request):
    if request.method == "POST":
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        marca = request.POST.get('marca')
        fechaven = request.POST.get('fechaven')

        # Comprobar si los campos están vacíos o solo contienen espacios
        code = espacios_vacios(codigo)
        name = espacios_vacios(nombre)
        mark = espacios_vacios(marca)
        venc = espacios_vacios(fechaven)


        if not (code and name and mark and venc) or not codigo.startswith("#"):
            error_message = "Todos los campos son obligatorios y no pueden estar vacíos o solo contener espacios, ademas el codigo empiece con #."
            return render(request, 'registro.html', context={'error_message': error_message})
        else:
            return redirect(reverse('validacion', kwargs={
                'codigo': codigo,
                'nombre': nombre,
                'marca': marca,
                'fechaven': fechaven
            }))

    return redirect('register')
