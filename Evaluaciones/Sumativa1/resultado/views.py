from django.shortcuts import render
import datetime
from consulta.views import productos

def convert_date(date_str):
    # Suponemos que la fecha está en formato 'yyyy-mm-dd'
    try:
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        # Convertimos la fecha a formato 'dd/mm/yy'
        return date_obj.strftime('%d/%m/%y')
    except ValueError:
        return None 


def validacion(request, codigo, nombre, marca, fechaven):

    nuevafecha=str(convert_date(fechaven))
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