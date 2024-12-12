from django.db import IntegrityError
from ninja import NinjaAPI, Schema
from django.contrib.auth import authenticate
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from pydantic import ValidationError
from .utils import generar_token, JWTAuth
from inicio.models import Producto, Marca, Caracteristica, NombreCaracteristica, Categoria
from .schemas import AuthRequest, MarcaSchema, caracteristicaSchema, nombreCaracteristicaSchema, ProductoSchema,categoriaSchema,ErrorResponse
from typing import List

api = NinjaAPI(
    title="Api de productoraSA",
    description="Una serie de servicios para la gestión de productos, que permiten la creación, edición y eliminación de productos, marcas, categorías y características",
    version="1.0.0"
)

auth = JWTAuth()

@api.exception_handler(Http404)
def error_404(request, ex):
    return api.create_response(request, 
                               {'response': 'Recurso no encontrado'},
                               status=404)
    
@api.exception_handler(ValidationError)
def error_validacion(request, ex):
    return api.create_response(request,
                               {
                                   'response': 'Error de Formato de Entrada',
                                   'errores': ex.errors()
                               },
                               status=422)

@api.exception_handler(IntegrityError)
def error_integridad(request, ex):
    return api.create_response(request,
                               {'response': 'Error de Integridad'},
                               status=400)

@api.post(path="token/", tags=["Auth"])
def get_token(request, data: AuthRequest):
    """ Obtiene un token de autenticación si el usuario esta en el grupo admin_products, esto 
    le permitirá acceder a los servicios de la API """
    
    user = authenticate(username=data.username, password=data.password)
    if not user:
        return { "error": "Credenciales inválidas" }
    else:
        if user.groups.filter(name='admin_products').exists():
            return { "token": generar_token(user), "user": user}
        else:
            return { "error": "El usuario no tiene permisos" }

# GET-ALL / GET-ONE / DELETE / UPDATE / PUT

################ GET ######################
# Obtener objeto de la query y guardar los datos correspondientes en un json serializable
@api.get("all/", tags=["ALL"])
def get_products(request):
    """Obtiene todos los productos de la base de datos para ser presentados en el frontend"""
    try:
        productos = Producto.objects.select_related('marca', 'categoria').prefetch_related("caracteristicas").all()
        all_products = []
        for producto in productos:
            caract = {}
            for caracteristica in producto.caracteristicas.all():  # Access related caracteristicas
                caract[str(caracteristica.nombre)] = str(caracteristica.descripcion)

            product = {
                "id": producto.id,
                "codigo": producto.codigo,
                "marca": producto.marca.nombre,
                "nombre": producto.nombre,
                "precio": producto.precio,
                "caracteristicas": caract,
                "categoria": producto.categoria.nombre
            }
            all_products.append(product)
            
        return all_products
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)


# GET one product
@api.get(path="product/{pid}",tags=["products"])
def get_product(request,pid:int):
    """Obtiene un producto en específico de la base de datos"""
    one_product = get_object_or_404(Producto,id=pid)
    return list(one_product)

#################################################

############### DELETE ############################
@api.delete(path="delete/{pid}",tags=["products"])
def del_product(request,pid:int):
    """Elimina un producto en específico de la base de datos según su id"""
    try:
        delete_product = Producto.objects.get(id=pid)
        producto_el,_ = delete_product.delete()
        if producto_el >0:
            return {"sucess":True,"message":"Objeto eliminado correctamente"}
    except:
        return {"success":False,"message":"El objeto no existe"}


############# PUT FROM ID ######################
@api.put("edit/{pid}",tags=["products"])
def edit(request,pid:int,data:Schema):
    """Edita un producto en específico de la base de datos (No implementado)"""
    product = get_object_or_404(Producto,id=pid)
    for attr,value in data.dict().items():
        setattr(product,attr,value)
    product.save()
    return {"id":pid,"title":product.nombre}

################### POST ####################
@api.post("addmarca/", response={200: MarcaSchema, 400: ErrorResponse})
def new_marca(request, data: MarcaSchema):
    """Crea una nueva marca en la base de datos primero verificando si no existe anteriormente"""
    if Marca.objects.filter(nombre=data.nombre).exists():
        return 400, {"error": "La marca ya existe"}
    
    try:
        # Crear una nueva instancia de Marca usando los datos proporcionados
        marca = Marca.objects.create(**data.dict())
    except IntegrityError:
        return 400, {"error": "Error de integridad al crear la marca"}
    return marca

@api.post("addcaracteristica/",response ={200:nombreCaracteristicaSchema,400:ErrorResponse})
def new_caracteristica(request,data:nombreCaracteristicaSchema):
    """Crea una nueva caracteristica en la base de datos primero verificando si no existe anteriormente"""
    if NombreCaracteristica.objects.filter(nombre=data.nombre).exists():
        return 400, {"error": "La caracteristica ya existe"}
    
    caracteristica = NombreCaracteristica.objects.create(**data.dict())
    return caracteristica

@api.post("addcategoria/",response={200:categoriaSchema,400:ErrorResponse})
def new_categoria(request,data:categoriaSchema):
    """Crea una nueva categoria en la base de datos primero verificando si no existe anteriormente"""
    if Categoria.objects.filter(nombre=data.nombre).exists():
        return 400, {"error": "La categoria ya existe"}
    
    categoria = Categoria.objects.create(**data.dict())
    return categoria

@api.post("addproducto/", response={200:ProductoSchema,400:ErrorResponse},tags=["products"])
def new_producto(request,data:ProductoSchema):
    """Crea un nuevo producto en la base de datos verificando si el código o nombre ya existen"""
    if Producto.objects.filter(codigo=data.codigo).exists():
        return 400, {"error": "El código ya existe"}
    if Producto.objects.filter(nombre=data.nombre).exists():
        return 400, {"error": "El nombre ya existe"}
    
    marca = Marca.objects.get(id=data.marca)
    categoria = Categoria.objects.get(id=data.categoria)
    
    producto = Producto.objects.create(
        codigo=data.codigo,
        marca=marca,
        nombre=data.nombre,
        precio=data.precio,
        categoria=categoria)
    
    if data.caracteristicas:
        for caracteristica in data.caracteristicas:
            caracteristica = Caracteristica.objects.filter(id=caracteristica).first()
            producto.caracteristicas.add(caracteristica.id)
        producto.save()
        
    return producto.id
    
@api.post("addcaracteristicas",response=caracteristicaSchema)
def new_caracteristica_for_product(request,data: List[dict]):
    if Caracteristica.objects.filter(nombre=data.nombre).exists():
        return 400, {"error": "La caracteristica ya existe"}
    ids = []
    if len(data) > 0:
        for caracteristica in data.caracteristicas:
            nombre_carac = NombreCaracteristica.objects.get(id=data.nombre) 
            caracteristica_new = Caracteristica.objects.create(nombre=nombre_carac,descripcion=data.descripcion)
            ids.append(caracteristica_new.id)
        return {'id':ids}
    else:
        return 204, {"no-content": "No se han ingresado datos"}
    