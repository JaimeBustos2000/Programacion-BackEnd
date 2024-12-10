from django.urls import path,include
from .views import main,auth,login_page,registrar_page,create_user,logout_page,info

urlpatterns = [    
    path("",login_page,name="login"),
    path("inicio/",main,name="main"),
    path("nuevo/",registrar_page,name="registrarpage"),
    path("nuevoUsuario",create_user,name="create_user"),
    path("auth/",auth,name="auth"),
    path("logout/",logout_page,name="logout"),
    path("info/",info,name="info")
]