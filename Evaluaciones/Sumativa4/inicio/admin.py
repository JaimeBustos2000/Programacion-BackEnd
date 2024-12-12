from django.contrib import admin
from inicio.models import Categoria,Caracteristica,Producto,Marca,NombreCaracteristica


admin.site.register(Categoria)
admin.site.register(NombreCaracteristica)
admin.site.register(Caracteristica)
admin.site.register(Producto)
admin.site.register(Marca)
