from ninja import Schema,ModelSchema
from ninja.orm import create_schema
from inicio.models import Producto, Marca, Caracteristica, NombreCaracteristica, Categoria
from typing import Optional

class AuthRequest(Schema):
    """Esquema de autenticación para revision con Jwt"""
    username: str
    password: str
    
class ErrorResponse(Schema):
    """Esquema de respuesta de error"""
    error : str

class patch_schema(Schema):
    """Esquema de patch"""
    marca_id: Optional[int] = None
    categoria_id: Optional[int] = None
    nombre: Optional[str] = None
    precio: Optional[int] = None

MarcaSchema = create_schema(Marca,exclude=['id'])
MarcaSchema.__doc__ = "Esquema de Marca con id autogenerado"

categoriaSchema = create_schema(Categoria,exclude=['id'])
categoriaSchema.__doc__ = "Esquema de Categoria con id autogenerado"

nombreCaracteristicaSchema = create_schema(NombreCaracteristica,exclude=['id'])
nombreCaracteristicaSchema.__doc__ = "Esquema de NombreCaracteristica con id autogenerado"

caracteristicaSchema = create_schema(Caracteristica,depth=1,exclude=['id'])
caracteristicaSchema.__doc__ = "Esquema de Caracteristica con id autogenerado y relaciones con NombreCaracteristica"

ProductoSchema = create_schema(Producto,exclude=['id'])
ProductoSchema.__doc__ = "Esquema de Producto con id autogenerado y relaciones con Marca, Categoria y Caracteristica" 
