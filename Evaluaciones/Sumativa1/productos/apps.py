from django.apps import AppConfig


class ProductosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'productos'

"""
class productos():
    def __init__(self):
        self.lista_productos = []

    def caracteristicas():
        self.codigo = codigo
        self.nombre = nombre
        self.marca = marca
        self.fecha_vencimiento = fvencimiento

        return self.codigo, self.nombre, self.marca, self.fecha_vencimiento
        
    def mostrar(self):
        return self.lista_productos
    
    def agregar(self, codigo, nombre, marca, fvencimiento):
    
        self.lista_productos.append(self.caracteristicas())
    
    
"""