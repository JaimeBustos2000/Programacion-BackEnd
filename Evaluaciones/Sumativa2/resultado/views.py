from django.shortcuts import render
import datetime
from consulta.views import productos

def convertir_fecha(date_str):
    try:
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%d/%m/%y')
    except ValueError:
        return None 

def validacion(request, codigo, nombre, marca, fechaven):

    nuevafecha=str(convertir_fecha(fechaven))
    productos.append({
            'codigo': codigo,
            'nombre': nombre,
            'marca': marca,
            'fechaven': nuevafecha
        })

    
    return render(request, 'resultado.html', {
        'codigo': codigo,
        'nombre': nombre,
        'marca': marca,
        'fechaven': nuevafecha
    })