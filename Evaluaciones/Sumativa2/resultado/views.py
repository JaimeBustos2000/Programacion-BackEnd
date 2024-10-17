from django.shortcuts import render
from inicio.models import Producto


def validacion(request,codigo):
    try:
        producto = Producto.objects.get(codigo=codigo)
    except Producto.DoesNotExist:
        producto = None
    finally:
        context = {
            'producto': producto,
        }
        
    return render(request, 'resultado.html', context=context)