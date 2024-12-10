from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.register,name="register"),
    path('registrado/', views.registrado, name='registrado'),
    path('nuevaMarca/', views.nuevaMarca, name='nuevaMarca'),
    path('nuevaCategoria/', views.nuevaCategoria, name='nuevaCategoria'),
    path('nuevaCaracteristica/', views.nuevaCaracteristica, name='nuevaCaracteristica'),
    path('validacion/', include("resultado.urls"), name='validacion')
]