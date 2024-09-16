# Create your views here.
from django.shortcuts import render,redirect,HttpResponse

def main(request):
    context=[
    {"codigo":'#12340',"nombre":"Jugo de frambuesa","marca":"Livean","fechaven":"12/03/25"},
    {"codigo":'#23338',"nombre":"Mantequilla","marca":"Soprole","fechaven":"11/05/25"},
    {"codigo":'#13336',"nombre":"Jamon serrano","marca":"SuperCerdo","fechaven":"12/06/25"},
    {"codigo":'#12354',"nombre":"Pack de huevos","marca":"Dicorne","fechaven":"12/12/25"},
    {"codigo":'#11243',"nombre":"Queso mantecoso","marca":"Colun","fechaven":"11/2/25"},
    {"codigo":'#12352',"nombre":"Leche sin lactosa","marca":"Colun","fechaven":"09/01/25"},
    {"codigo":'#12342',"nombre":"Galletas de chocolate","marca":"Costa","fechaven":"20/5/25"},
    {"codigo":'#12343',"nombre":"Bebida de fantasia","marca":"Fruna","fechaven":"10/5/25"},
    {"codigo":'#12341',"nombre":"Manzanas","marca":"Envy","fechaven":"01/04/25"},
    {"codigo":'#12344',"nombre":"Pan de Molde","marca":"Ideal","fechaven":"22/7/25"},
    {"codigo":'#12345',"nombre":"Carne de vacuno","marca":"Cousine and Co","fechaven":"15/03/25"},
    {"codigo":'#12347',"nombre":"Yogurth de vainilla","marca":"Danone","fechaven":"16/04/25"}]

    return render(request,"productos.html",context=context)