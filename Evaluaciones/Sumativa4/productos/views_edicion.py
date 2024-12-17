
from inicio.models import Marca, Caracteristica, NombreCaracteristica, Categoria, Producto
from django.shortcuts import render
import requests
from  django.contrib.auth.decorators import login_required, user_passes_test
from inicio.views import is_in_group_any, is_in_group
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.http import JsonResponse

@user_passes_test(is_in_group_any, login_url="/inicio/")
@login_required
def edicion_page(request, id):
    marcas = Marca.objects.all().order_by("nombre")
    categorias = Categoria.objects.all().order_by("nombre")
    caracteristicas = list(NombreCaracteristica.objects.all().order_by("nombre").values_list("nombre", flat=True))
    
    api_url = f"http://localhost:8000/productos/api/product/{id}"
    
    response = requests.get(api_url)
    if response.status_code == 200:
        producto = response.json()
        print(producto)
        return render(request,"detalles.html",context={
            "marcas":marcas,
            "categorias":categorias,
            "caracteristicas":caracteristicas,
            "producto":producto
            })
    
    else:
        return render(request,"consulta.html",context={"error":"No se encontró el producto"})

@user_passes_test(is_in_group, login_url="/inicio/")
@login_required
def edicion(request, id):
    product = get_object_or_404(Producto, id=id)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        marca_id = request.POST.get('marca')
        precio = request.POST.get('precio')
        categoria_id = request.POST.get('categoria')

        update_data = {}

        if nombre and nombre != product.nombre:
            update_data['nombre'] = nombre
        if marca_id and int(marca_id) != product.marca.id:
            update_data['marca_id'] = int(marca_id)
        if precio and int(precio) != product.precio:
            update_data['precio'] = int(precio)
        if categoria_id and int(categoria_id) != product.categoria.id:
            update_data['categoria_id'] = int(categoria_id)

        print(update_data)
        token = request.session.get('token')
        print(token)
        
        if update_data:
            response = requests.patch(
                f'http://localhost:8000/productos/api/patch/{id}',
                json=update_data,
                headers={'Authorization': f'Bearer {request.session['token']}'}
            )
            if response.status_code == 200:
                return redirect('productos')  
            else:
                print(response.json())
                return JsonResponse({'error': 'Error al editar el producto'}, status=response.status_code)
        else:
            if update_data['categoria_id'] and update_data['marca_id'] and update_data['nombre'] and update_data['precio']:
                response = requests.get(f'http://127.0.0.1:8000/productos/api/product/{id}')
                
                # Simula el put de la api obteniendo datos del producto que son mas complejos en este caso
                # La api put solo se ejecutara si los 4 elementos que estan editables en el form son
                # diferentes a los que ya estan en la base de datos
                if response.status_code == 200:
                    data = response.json()
                    
                    caracteristicas_ids = []
                    for key,value in data['caracteristicas'].items():
                        caracteristica = Caracteristica.objects.get(nombre_id=key,producto_id=id)
                        caracteristicas_ids.append(caracteristica.id)
                    
                    nuevo_producto_dict = {
                        'codigo' : data['codigo'],
                        'marca_id': data['marca'],
                        'nombre': update_data['nombre'],
                        'precio': update_data['precio'],
                        'categoria_id': data['categoria'],
                        'caracteristicas': caracteristicas_ids
                        
                    }
                    response_edit = requests.put(
                        f'http://127.0.0.1:8000/productos/api/edit/{id}',
                        json=nuevo_producto_dict,
                        headers={'Authorization': f'Bearer {request.session['token']}'})
                    
                    if response_edit.status_code == 200:
                        return redirect('productos', {'message': 'Producto editado correctamente'})
                    
                else:
                    return JsonResponse({'error': 'Error al editar el producto'}, status=response.status_code)
    else:
        return redirect('productos', {'error': 'Error al editar el producto'})