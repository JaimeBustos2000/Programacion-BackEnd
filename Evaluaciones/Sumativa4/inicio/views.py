from django.shortcuts import render, redirect
from .forms import UserForm, NewUser
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.password_validation import validate_password 
from django.db import IntegrityError
from .unauthdeco import unauthenticated_user
from datetime import *
import requests

############# Visor de grupo ##################
def is_in_group(group_name):
    def check(user):
        return user.groups.filter(name=group_name).exists()
    return check

def is_in_group_any(user):
    # Verifica si el usuario pertenece a uno de los grupos
    return user.groups.filter(name__in=['admin_products', 'individual']).exists()
############# Visor de grupo ##################

# Vista principal inicio (no es '/')
def main(request):
    return render(request,"index.html")

# Paginas de inicio de sesion y registro
@unauthenticated_user
def login_page(request):
    return render(request,"login.html",context={"login":UserForm()})

@unauthenticated_user
def registrar_page(request):
    return render(request,"registrarUsuario.html",context={"registro":NewUser()})

# Autenticacion de usuario y desconexión
def auth(request):
    login_form = UserForm(request.POST)
    if login_form.is_valid():
        usuario = login_form.cleaned_data["usuario"]
        contrasena = login_form.cleaned_data["contrasena"]
        
        if not User.objects.filter(username=usuario).exists():
            return render(request,"login.html",context={"login":login_form,"error":"Usuario no existe"})
        
        api_url = "http://localhost:8000/productos/api/token/"
        
        response = requests.post(api_url, json={"username":usuario,"password":contrasena})
        if response.status_code == 200 or response.status_code == 204:
            try:
                data = response.json()
                token = data.get('token')
            except:
                print("El usuario no puede obtener el token")
                token = None
            finally:
                user = authenticate(username=usuario, password=contrasena)
                login(request, user)
                session = request.session
                session["user"] = usuario
                session["admin_products"] = user.groups.filter(name="admin_products").exists()
                hora_sesion = datetime.utcnow()
                session['login_date'] = hora_sesion.strftime("%d-%m-%Y %H:%M:%S")
                if token is not None:
                    session['token'] = token
                    print(session['token'])
                    
            return redirect("main")
        else:
            return render(request,"login.html",context={"login":login_form,"error":"Usuario o contraseña incorrectos"})
        
    return render(request,"login.html",context={"login":login_form,"error":"Usuario o contraseña invalidos"})

@login_required
def logout_page(request):
    logout(request)
    return redirect("login")

# Creacion de usuarios nuevos
@unauthenticated_user
def create_user(request):
    nuevo_usuario=NewUser(request.POST)
    if nuevo_usuario.is_valid():
        usuario = nuevo_usuario.cleaned_data["usuario"]
        contrasena = nuevo_usuario.cleaned_data["contrasena"]
        email = nuevo_usuario.cleaned_data["email"]
        
        if not validate_password(contrasena):
            return render(request,"registrarUsuario.html",context={"registro":NewUser(),"error":"Contraseña poco segura o invalida"})
        
        try:
            user = User.objects.create_user(username=usuario,password=contrasena,email=email)
            return redirect("main")

        except IntegrityError:
            return render(request,"registrarUsuario.html",context={"registro":NewUser(),"error":"Usuario ya existe"})

@user_passes_test(is_in_group_any,login_url='main')
@login_required
def info(request):
    return render(request,"infosesion.html")