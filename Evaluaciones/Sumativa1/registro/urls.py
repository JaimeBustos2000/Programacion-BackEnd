from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.register,name="register"),
    path('registrado/', views.registrado, name='registrado'),
    path('validacion/', include("resultado.urls"), name='validacion')
]