from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.productos,name="productos"),
    path("consulta/",views.consulta,name="consulta"),
]