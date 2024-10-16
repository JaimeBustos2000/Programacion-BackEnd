from django.shortcuts import render
import datetime

def convertir_fecha(date_str):
    try:
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%d/%m/%y')
    except ValueError:
        return None 

def validacion(request,codigo):
    context = {
        'codigo': codigo,
    }
    return render(request, 'resultado.html', context=context)