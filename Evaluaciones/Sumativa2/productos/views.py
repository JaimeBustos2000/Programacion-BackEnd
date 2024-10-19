# Create your views here.
from django.shortcuts import render
from inicio.models import Producto, Categoria,NombreMarca,Marca,Caracteristica,OpcionCategoria,OpcionCaracterisca
from django.http import JsonResponse

def main(request):
    productos = Producto.objects.all().order_by('id')
    marcas = Marca.objects.all()
    categorias = Categoria.objects.all()
    caracteristicas = OpcionCaracterisca.objects.all()
    
    context = {
        'productos': productos,
        'marcas': marcas,
        'categorias': categorias,
        'caracteristicas': caracteristicas,
    }
    return render(request, 'consulta.html', context)

def consulta(request):
    productos = Producto.objects.all()
    marcas = Marca.objects.all()
    categorias = Categoria.objects.all()
    caracteristicas = OpcionCaracterisca.objects.all()
    
    print("Productos: ", productos)
    if request.method == 'POST':
        categoria = request.POST.get('categoria')
        marca = request.POST.get('marca')
        orden_precio = request.POST.get('precio')
        caracteristicas_ids = request.POST.getlist('caracteristicas[]')
        
        caracteristicas_ids = [int(caracteristica) for caracteristica in caracteristicas_ids]
        
        if categoria:
            print("Hay filtro de categoria")
            productos = productos.filter(categoria__nombre=categoria)
        if marca:
            print("Hay filtro de marca")
            productos = productos.filter(marca__nombre=marca)
            
        if orden_precio:
            if orden_precio == 'asc':
                productos = productos.order_by('precio')
            else:
                productos = productos.order_by('-precio')
        else:
            productos = productos.order_by('id')
    
    
        if caracteristicas_ids:
            print("Hay filtro de características")
            print("caracteristicas: ", caracteristicas_ids)
            
            id_productos_filtrados = []
            
            for producto in productos:
                print("Producto: ", producto)
                # Obtener las características asociadas del producto
                caracteristicas_asociadas = producto.caracteristicas.all()
                print("Características asociadas: ", caracteristicas_asociadas)
                
                # Obtener las ids de las caracteristicas con detalles
                caracteristicas_producto = []
                for caracteristica in caracteristicas_asociadas:
                    print("--------------------")
                    id_caracteristica = int(Caracteristica.objects.get(id=caracteristica.id).nombre_id)
                    caracteristicas_producto.append(id_caracteristica)
                    print("Características id referenciada: ", id_caracteristica)
                    print("nombre de la caracteristica:",OpcionCaracterisca.objects.get(id=id_caracteristica).nombre)
                    print("--------------------")
                print("Características producto: ", caracteristicas_producto)
                
                todas_coinciden = True
                if all(item in caracteristicas_producto for item in caracteristicas_ids):
                    print("Características coinciden")
                    id_productos_filtrados.append(producto.id)
                    todas_coinciden = True
                else:
                    todas_coinciden = False
                    print("Características no coinciden")
                    
                print("lista de productos filtrados: ", id_productos_filtrados)
                
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