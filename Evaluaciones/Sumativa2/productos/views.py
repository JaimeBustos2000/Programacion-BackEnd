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