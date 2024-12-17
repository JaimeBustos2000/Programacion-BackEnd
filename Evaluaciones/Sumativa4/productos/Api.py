from django.db import IntegrityError,transaction
from ninja import NinjaAPI, Schema
from django.contrib.auth import authenticate
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from pydantic import ValidationError
from .utils import generar_token, JWTAuth, generar_token_generico
from inicio.models import Producto, Marca, Caracteristica, NombreCaracteristica, Categoria
from .schemas import AuthRequest, MarcaSchema, nombreCaracteristicaSchema, ProductoSchema,categoriaSchema,ErrorResponse,patch_schema
from datetime import *
from ninja.errors import HttpError
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from django.contrib.admin.views.decorators import staff_member_required

# 127:0.0.1:8000/productos/api/docs
# Esquemas autogenerados para la API de productos para mayor info de las clases ver schemas.py y inicio/models.py
auth = JWTAuth()

# Vista protegida para el administrador de productos
api = NinjaAPI(
    title="Api de productoraSA",
    description="Una serie de servicios para la gestión de productos autorizados segun jwt para el grupo admin_products, que permiten la obtencion(GET), creación(POST), actualizacion parcial(PATCH), actualizacion con sobreescritura(PUT) y eliminación de productos(DELETE). Además de la creación de marcas, categorias y caracteristicas(nombres)",
    version="1.0.0",
    docs_decorator = staff_member_required,
    auth=auth,
)

# Por alguna extraña razón, la seccion authorized de swagger no funciona correctamente, pero si
# se accede a la API con un token válido usando la misma api disponible, se puede acceder a los servicios de la API desde docs.


# Parcialmente implementado patch y put, dado la complejidad de las relaciones entre las tablas, 
# se optó por no implementarlos completamente

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
    
@api.exception_handler(Exception)
def error_general(request, ex):
    return api.create_response(request,
                               {'response': 'Error interno del servidor'},
                               status=500)

@api.exception_handler(HttpError)
def unauthorized(request, ex):
    return api.create_response(request,
                               {'response': 'No autorizado. Credenciales inválidas'},
                               status=401)
    
@api.exception_handler(NotImplementedError)
def not_implemented(request, ex):
    return api.create_response(request,
                               {'response': 'Función no implementada'},
                               status=501)
    

@api.post(path="token/", tags=["Auth"],auth=None)
def get_token(request, data: AuthRequest):
    """Obtiene un token de autenticación si el usuario está en el grupo admin_products,
    esto le permitirá acceder a los servicios de la API\n
    
    Params: como parámetros un nombre de usuario y una contraseña\n
    
    Return admin_products :  token de autenticación si el usuario está en el grupo admin_products.\n
    Return usuario no apto :  token generico. No apto para funciones dentro de la api\n
    """
    user = authenticate(username=data.username, password=data.password)
    if not user:
        return JsonResponse({"error": "Usuario o contraseña incorrectos"}, status=401)

    if user.groups.filter(name='admin_products').exists():
        print("Usuario en grupo admin_products")
        return JsonResponse({"token": generar_token(user), "status": 200})
    else:
        print("Usuario no apto")
        return JsonResponse({"token": generar_token_generico(user), "status": 200})

################ GET ######################

# Obtener objeto de la query y guardar los datos correspondientes en un json serializable
@api.get("all/", 
        tags=["ALL"],
        auth=None,
        summary="Obtiene todos los productos de la base de datos",
        description="""Obtiene todos los productos de la base de datos para ser presentados en el frontend\n
                    No recibe parametros\n
                    Return: todos los productos de la base de datos\n"""
        )
def get_products(request):
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
        return JsonResponse({'error': 'Productos no encontrados'}, status=404)


# GET un producto en específico
@api.get(path="product/{pid}", 
         tags=["products"],
         auth=None,
         summary="Obtiene un producto en específico de la base de datos",
         description=
        """Mediante una peticion que requiere un id, no requiere token, solo para metodos "generales"\n
        params: pid (int) - id del producto a obtener\n
        Return: producto especifico de la base de datos serializado\n
        """)
def get_product(request, pid: int):

    try:
        # Optimiza la consulta usando select_related y prefetch_related
        one_product = Producto.objects.select_related('marca', 'categoria').prefetch_related("caracteristicas").get(id=pid)
        
        # Construir el diccionario de respuesta manualmente
        one_product_dict = {
            'id': one_product.id,
            'codigo': one_product.codigo,
            'marca': one_product.marca.nombre,  # Solo el nombre de la marca
            'nombre': one_product.nombre,
            'precio': one_product.precio,
            'categoria': one_product.categoria.nombre,  # Solo el nombre de la categoría
        }

        # Procesar las características
        caract = {}
        if one_product.caracteristicas != []:
            for caracteristica in one_product.caracteristicas.all().values():
                nombre_de_caracteristica = str(NombreCaracteristica.objects.get(id=caracteristica['nombre_id']).nombre)
                caract[nombre_de_caracteristica] = caracteristica['descripcion']

            one_product_dict['caracteristicas'] = caract
        else:
            one_product_dict['caracteristicas'] = ""
        
        return JsonResponse(one_product_dict)
    except Producto.DoesNotExist:
        print("Producto no encontrado")
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    except Exception as e:
        # Log the exception details
        print(f"Error: {e}")
        return JsonResponse({'error': 'Error interno del servidor'}, status=500)

############### DELETE ############################
@api.delete(path="delete/{pid}", 
            tags=["products"],
            auth=auth,
            summary="Elimina un producto en específico de la base de datos",
            description="""
    Elimina un producto en específico de la base de datos según su id, requiere un token autorizado\n
    params: pid (int) - id del producto a eliminar\n
    Return: mensaje de éxito si el producto fue eliminado con éxito y status 200\n
    Return: error si el producto no fue encontrado y status 404\n
    """)
def del_product(request, pid: int):
    try:
        producto = Producto.objects.get(id=pid)
        producto.delete()
        return JsonResponse({"message": "Producto eliminado con éxito"}, status=200)
    
    except Producto.DoesNotExist:
        return JsonResponse({"error": "Producto no encontrado"}, status=404)


############# PUT FROM ID ###################### (No implementado)
@api.put("edit/{pid}",
         tags=["products"],
         auth=auth,
         summary="Sobreescribe un producto en específico",
         description="""
         Edita un producto en específico de la base de datos sobrescribiendo los datos\n
         params: pid (int) - id del producto a editar\n
         params: data (ProductoSchema) - datos del producto a editar(recibe datos con el formato del esquema) inicio/models.py\n
            Return: producto editado con éxito y status 200\n
            Return: error si el producto no pudo ser editado y status 400\n
         """)
def edit(request,pid:int,data:ProductoSchema):
    try:
        product = get_object_or_404(Producto,id=pid)
        for attr,value in data.dict().items():
            setattr(product,attr,value)
        product.save()
        return {"id":pid,"title":product.nombre}
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({"error": f"Error al editar el producto: {str(e)}"}, status=400)


########## PATCH FROM ID ############################
@api.patch("patch/{pid}",
           tags=["products"],
           auth=auth,
           summary="Edita un producto en específico con ciertos atributos presentes o no",
           description=
            """Edita un unico producto y actualiza solo los datos proporcionados\n
            optional params: marca_id (int) - id del producto a editar\n
            ---------------- categoria_id (id) - nombre del producto\n
            ---------------- nombre (str) - nombre del producto\n
            ---------------- precio (int) - precio del producto\n
            Return: producto editado con éxito y status 200\n
            Return: error si el producto no pudo ser editado y status 400\n
            """)
def patch_product(request,pid:int,data:patch_schema):
    try:
        product = get_object_or_404(Producto,id=pid)
        update_data = data.dict(exclude_unset=True)
        for attr,value in update_data.items():
            setattr(product,attr,value)
        product.save()
        
        return JsonResponse({
            "id":pid,
            "title":product.nombre,
            "marca":product.marca.nombre,
            "categoria":product.categoria.nombre,
            "precio":product.precio
            },status=200)
        
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({"error": f"Error al editar el producto: {str(e)}"}, status=400)



################### POST ####################
@api.post("addmarca/", 
          response={200: MarcaSchema, 400: ErrorResponse},
          auth=auth, 
          tags=["marca"],
          summary="Crea una nueva marca en la base de datos",
          description="""Crea una nueva marca en la base de datos primero verificando si no existe anteriormente\n
            params: data (MarcaSchema) - datos de la marca a crear(recibe datos con el formato del esquema) inicio/models.py\n
            Return: marca creada con éxito y status 200\n
            Return: error si la marca ya existe y status 400\n
            """)
def new_marca(request, data: MarcaSchema):
    if Marca.objects.filter(nombre=data.nombre).exists():
        return JsonResponse({"error": "La marca ya existe"}, status=400)
    
    try:
        # Crear una nueva instancia de Marca usando los datos proporcionados
        marca = Marca.objects.create(**data.dict())
    except IntegrityError:
        return JsonResponse({"error": "Error al crear la marca"}, status=400)
    return marca

@api.post("addcaracteristica/",
          response ={200:nombreCaracteristicaSchema,400:ErrorResponse},
          auth=auth,
          tags=["caracteristica"],
          summary="Crea una nueva caracteristica en la base de datos",
          description="""Crea una nueva caracteristica en la base de datos primero verificando si no existe anteriormente\n
            params: data (nombreCaracteristicaSchema) - datos de la caracteristica a crear(recibe datos con el formato del esquema) inicio/models.py\n
            Return: caracteristica creada con éxito y status 200\n
            Return: error si la caracteristica ya existe y status 400, mas el error mostrado con un esquema\n
            """)
def new_caracteristica(request,data:nombreCaracteristicaSchema):
    if NombreCaracteristica.objects.filter(nombre=data.nombre).exists():
        return JsonResponse({"error": "La característica ya existe"}, status=400)
    
    caracteristica = NombreCaracteristica.objects.create(**data.dict())
    return caracteristica

@api.post("addcategoria/",
          response={200:categoriaSchema,400:ErrorResponse},
          auth=auth, 
          tags=["categoria"],
          summary="Crea una nueva categoria en la base de datos",
          description="""Crea una nueva categoria en la base de datos primero verificando si no existe anteriormente\n
            params: data (categoriaSchema) - datos de la categoria a crear(recibe datos con el formato del esquema) inicio/models.py\n
            Return: categoria creada con éxito y status 200\n
            Return: error si la categoria ya existe y status 400\n
            """)
def new_categoria(request,data:categoriaSchema):
    if Categoria.objects.filter(nombre=data.nombre).exists():
        return JsonResponse({"error": "La categoría ya existe"}, status=400)
    
    categoria = Categoria.objects.create(**data.dict())
    return categoria


from django.db import transaction

@api.post("addproducto/", 
          response={200: ProductoSchema, 400: ErrorResponse}, 
          tags=["products"],
          auth=auth,
          summary="Crea un nuevo producto en la base de datos",
          description="""Crea un nuevo producto en la base de datos verificando si el código o nombre ya existen\n
            params: data (ProductoSchema) - datos del producto a crear(recibe datos con el formato del esquema) inicio/models.py\n
            Return: producto creado con éxito y status 200\n
            Return: error si el codigo producto ya existe y status 404\n
            Return: error si la marca no existe y status 404\n
            Return: error si la categoria no existe y status 404\n
            Return: error si la caracteristica no existe y status 400\n
            Return: error interno del servidor y status 500\n
            """)
def new_producto(request, data: ProductoSchema):
    data = data.dict()
    print(data)
    try:
        if Producto.objects.filter(codigo=data['codigo']).exists():
            print("El código ya existe")
            return JsonResponse({"error": "El código ya existe"}, status=404)

        if Producto.objects.filter(nombre=data['nombre']).exists():
            print("El nombre ya existe")
            return JsonResponse({"error": "El nombre ya existe"}, status=404)

        try:
            marca = Marca.objects.get(id = data['marca'])
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Marca no encontrada"}, status=404)

        try:
            categoria = Categoria.objects.get(id = data["categoria"])
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Categoría no encontrada"}, status=404)

        with transaction.atomic():
            producto = Producto.objects.create(
                codigo=data['codigo'],
                marca=marca,
                nombre=data['nombre'],
                precio=data['precio'],
                categoria=categoria
            )

            if data['caracteristicas']:
                for caracteristica_id in data['caracteristicas']:
                    try:
                        caracteristica = Caracteristica.objects.get(id=caracteristica_id)
                        producto.caracteristicas.add(caracteristica.id)
                    except ObjectDoesNotExist:
                        print(f"Característica con ID {caracteristica_id} no encontrada")
                        return JsonResponse({"error": "Característica no encontrada"}, status=404)

            producto.save()
            return JsonResponse({"message": "Producto creado con éxito", "id": producto.id}, status=200)

    except ValueError as ve:
        return JsonResponse({"error": str(ve)}, status=400)
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({"error": f"Error al crear el producto: {str(e)}"}, status=500)