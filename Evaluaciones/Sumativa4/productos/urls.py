from django.urls import path,include
from . import views
from .Api import api

urlpatterns = [
    path("",views.productos,name="productos"),
    path("consulta/",views.consulta,name="consulta"),
    path("api/",api.urls)
]