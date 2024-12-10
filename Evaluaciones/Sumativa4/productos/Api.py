from ninja import NinjaAPI, Schema
from django.contrib.auth import authenticate
from django.http import HttpRequest, Http404
from django.shortcuts import get_object_or_404
from pydantic import ValidationError
from .utils import generar_token, JWTAuth
from inicio.models import Producto
from django.http import JsonResponse
from typing import List

api = NinjaAPI(
    title="Api de productoraSA",
    description="Se presentan los servicios con los cuales el sistema interactua",
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


class AuthRequest(Schema):
    username: str
    password: str



@api.post(path="/token", tags=["Auth"])
def get_token(request, data: AuthRequest):
    user = authenticate(username=data.username, password=data.password)
    if not user:
        return { "error": "Credenciales inválidas" }
    token = generar_token(user)
    return { "token": token }

# GET ALL / GET ONE / DELETE / UPDATE /

@api.get(path="all/",tags=["ALL"])
def get_products(request):
    all_products = Producto.objects.all().order_by().values()
    return list(all_products)

@api.get(path="product/{pid}",tags=["products"])
def get_product(request,pid:int):
    one_product = Producto.objects.filter(id=pid).values()
    return list(one_product)

@api.delete(path="delete/{pid}",tags=["products"])
def del_product(request,pid:int):
    try:
        delete_product = Producto.objects.get(id=pid)
        producto_el,_ = delete_product.delete()
        if producto_el >0:
            return {"sucess":True,"message":"Objeto eliminado correctamente"}
    except:
        return {"success":False,"message":"El objeto no existe"}

@api.patch("edit/{pid}",tags=["products"])
def edit(request,pid:int,data:Schema):
    product = get_object_or_404(Producto,id=pid)
    for attr,value in data.dict().items():
        setattr(product,attr,value)
    product.save()
    return {"id":pid,"title":product.nombre}

