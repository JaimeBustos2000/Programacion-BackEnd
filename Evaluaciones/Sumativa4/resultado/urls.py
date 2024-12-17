from django.urls import path
from . import views

urlpatterns = [
    #recibe un int id como parametro
    path('<int:id>/', views.validacion, name='validacion')
]