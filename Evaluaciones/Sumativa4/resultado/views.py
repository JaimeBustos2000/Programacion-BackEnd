from django.shortcuts import render
from inicio.models import Producto
from django.contrib.auth.decorators import login_required,user_passes_test

############# Visor de grupo ##################
def is_in_group(group_name):
    def check(user):
        return user.groups.filter(name=group_name).exists()
    return check

############# Visor de grupo ##################

@login_required
@user_passes_test(is_in_group('admin_products'),login_url='main')
def validacion(request,codigo):
    try:
        producto = Producto.objects.get(codigo=codigo)
    except Producto.DoesNotExist:
        producto = None
    finally:
        context = {
            'producto': producto,
        }
        
    return render(request, 'resultado.html', context=context)