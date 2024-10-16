# Create your views here.
from django.shortcuts import render
from inicio.models import Producto, Categoria

def main(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    
    context = {
        'productos': productos,
    }
    
    return render(request, 'consulta.html', context)