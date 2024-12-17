from django.urls import path,include
from . import views_productos
from . import views_registro
from . import views_edicion
from .Api import api

urlpatterns = [
    path("",views_productos.productos_list,name="productos"),
    path("consulta/",views_productos.consulta,name="consulta"),
    path("registro/",views_registro.register_page,name="register_page"),
    path('registro/registrado/', views_registro.nuevo_producto, name='nuevoProducto'),
    path('registro/nuevaMarca/', views_registro.nuevaMarca, name='nuevaMarca'),
    path('registro/nuevaCategoria/', views_registro.nuevaCategoria, name='nuevaCategoria'),
    path('registro/nuevaCaracteristica/', views_registro.nuevaCaracteristica, name='nuevaCaracteristica'),
    path('validacion/', include("resultado.urls"), name='validacion'),
    path('eliminar/<int:producto_id>/', views_productos.eliminar, name='eliminar'),
    path('detalles/<int:id>/', views_edicion.edicion_page, name='detalles'),
    path('detalles/editado/<int:id>', views_edicion.edicion, name='editado'),
    path("api/",api.urls)
]