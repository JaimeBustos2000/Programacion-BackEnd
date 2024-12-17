from django.shortcuts import render
import requests
from django.contrib.auth.decorators import login_required,user_passes_test

############# Visor de grupo ##################
def is_in_group(group_name):
    def check(user):
        return user.groups.filter(name=group_name).exists()
    return check

############# Visor de grupo ##################

@login_required
@user_passes_test(is_in_group('admin_products'),login_url='main')
def validacion(request,id):
    print("ID:",id)
    id = int(id)
    api_url = f'http://127.0.0.1:8000/productos/api/product/{id}'
    response = requests.get(api_url)
    print("Response en validacion:",response.status_code)
    if response.status_code == 200:
        producto = response.json()
        print("Producto:",producto)
        return render(request, 'resultado.html', context={ 
            'producto': producto
        })
    else:
        return render(request, 'resultado.html', context={ 
            'producto': None
        })