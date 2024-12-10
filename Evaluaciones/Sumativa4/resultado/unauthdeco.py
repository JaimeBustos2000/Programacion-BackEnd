from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from functools import wraps

def unauthenticated_user(view_func):
    @wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main')  # Cambia 'home' por la URL a la que deseas redirigir a los usuarios autenticados
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
