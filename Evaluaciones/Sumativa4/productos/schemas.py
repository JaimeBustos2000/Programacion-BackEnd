from ninja import Schema,ModelSchema
from ninja.orm import create_schema
from inicio.models import Producto, Marca, Caracteristica, NombreCaracteristica, Categoria

class AuthRequest(Schema):
    """Esquema de autenticación para revision con Jwt"""
    username: str
    password: str
    
class ErrorResponse(Schema):
    """Esquema de respuesta de error"""
    error : str

MarcaSchema = create_schema(Marca,exclude=['id'])
MarcaSchema.__doc__ = "Esquema de Marca"

categoriaSchema = create_schema(Categoria,exclude=['id'])
categoriaSchema.__doc__ = "Esquema de Categoria"

nombreCaracteristicaSchema = create_schema(NombreCaracteristica,exclude=['id'])
nombreCaracteristicaSchema.__doc__ = "Esquema de NombreCaracteristica"

caracteristicaSchema = create_schema(Caracteristica,depth=1,exclude=['id'])
caracteristicaSchema.__doc__ = "Esquema de Caracteristica"

ProductoSchema = create_schema(Producto,exclude=['id'])
ProductoSchema.__doc__ = "Esquema de Producto"
