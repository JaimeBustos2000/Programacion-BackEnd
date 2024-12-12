# Create your views here.
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
import requests
from inicio.models import Producto, Categoria,Marca,Caracteristica
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse

############# Visor de grupo ##################
def is_in_group(group_name):
    def check(user):
        return user.groups.filter(name=group_name).exists()
    return check

def is_in_group_any(user):
    # Verifica si el usuario pertenece a uno de los grupos
    return user.groups.filter(name__in=['admin_products', 'individual']).exists()
############# Visor de grupo ##################


# Vista principal de productos donde se muestran la lista de productos
@user_passes_test(is_in_group_any,login_url='main')
@login_required
def productos_list(request):
    mensaje = request.GET.get('mensaje',None)
    response = requests.get('http://127.0.0.1:8000/productos/api/all')
    if response.status_code == 200:
        data = response.json()
    else:
        return JsonResponse({"Error":"No se pudieron obtener los datos de la api","message":"Solicitud no satisfactoria"})
    marcas = Marca.objects.all()
    categorias = Categoria.objects.all()
    caracteristicas = Caracteristica.objects.all()
    
    context = {
        'productos': data,
        'marcas': marcas,
        'categorias': categorias,
        'caracteristicas': caracteristicas,
        'mensaje': mensaje
    }
    return render(request, 'consulta.html', context)


# Vista de consulta de productos con permisos de consulta
@user_passes_test(is_in_group_any,login_url='main')
@login_required
def consulta(request):
    productos = Producto.objects.all()
    marcas = Marca.objects.all()
    categorias = Categoria.objects.all()
    caracteristicas = Caracteristica.objects.all()
    
    print("Productos: ", productos)
    if request.method == 'POST':
        categoria = request.POST.get('categoria')
        marca = request.POST.get('marca')
        orden_precio = request.POST.get('precio')
        caracteristicas_ids = list(request.POST.get('caracteristicas_ids').strip().split(','))
        
        # print("caracteristicas_ids: ", caracteristicas_ids)
        try:
            caracteristicas_ids = [int(caracteristica) for caracteristica in caracteristicas_ids]
        except ValueError:
            caracteristicas_ids = []
        
        if categoria:
            # print("Hay filtro de categoria")
            productos = productos.filter(categoria__nombre=categoria)
        if marca:
            # print("Hay filtro de marca")
            productos = productos.filter(marca__nombre=marca)
            
        if orden_precio:
            if orden_precio == 'asc':
                productos = productos.order_by('precio')
            else:
                productos = productos.order_by('-precio')
        else:
            productos = productos.order_by('id')
    
        if caracteristicas_ids:
            id_productos_filtrados = []
            
            for producto in productos:
                # Obtener las características asociadas del producto
                caracteristicas_asociadas = producto.caracteristicas.all()
                
                # Obtener las ids de las caracteristicas asociadas y buscar la referencia en las tablas relacionadas
                caracteristicas_producto = []
                for caracteristica in caracteristicas_asociadas:
                    # print("--------------------")
                    id_caracteristica = int(Caracteristica.objects.get(id=caracteristica.id).nombre_id)
                    caracteristicas_producto.append(id_caracteristica)
                    # print("Características id referenciada: ", id_caracteristica)
                    # print("nombre de la caracteristica:",OpcionCaracterisca.objects.get(id=id_caracteristica).nombre)
                
                # Verificar las coincidencias de id en las tablas
                if all(item in caracteristicas_producto for item in caracteristicas_ids):
                    id_productos_filtrados.append(producto.id)
                    
            # Filtrar los productos obtenidos   
            productos = productos.filter(id__in=id_productos_filtrados)
        
            return render(request, 'consulta.html', context={
                'productos': productos, 
                'marcas': marcas, 
                'categorias': categorias, 
                'caracteristicas': caracteristicas}) 
        else:
            return render(request, 'consulta.html', context={
                'productos': productos, 
                'marcas': marcas, 
                'categorias': categorias, 
                'caracteristicas': caracteristicas})
    context = {
        'productos': productos,
        'marcas': marcas,
        'categorias': categorias,
        'caracteristicas': caracteristicas,
    }
    
    return render(request, 'consulta.html', context)


# Vista de eliminación de productos con permisos de eliminación
@user_passes_test(is_in_group('admin_products'), login_url='main')
@login_required
def eliminar(request, producto_id):
    response = requests.delete(f'http://127.0.0.1:8000/productos/api/delete/{producto_id}')
    
    if response.status_code == 200:
        return redirect(f"{reverse('productos')}?mensaje=Producto eliminado")
    else:
        return redirect(f"{reverse('productos')}?mensaje=Error al eliminar el producto")

    
