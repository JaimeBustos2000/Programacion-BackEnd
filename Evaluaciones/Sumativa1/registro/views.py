from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse

def register(request):
    return render(request, 'registro.html')

def registrado(request):
    if request.method == "POST":
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        marca = request.POST.get('marca')
        fechaven = request.POST.get('fechaven')

        return redirect(reverse('validacion', kwargs={
            'codigo': codigo,
            'nombre': nombre,
            'marca': marca,
            'fechaven': fechaven
        }))

    return redirect('register')