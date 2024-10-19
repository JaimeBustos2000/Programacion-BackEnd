from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.main,name="register"),
    path("consulta/",views.consulta,name="consulta"),
]