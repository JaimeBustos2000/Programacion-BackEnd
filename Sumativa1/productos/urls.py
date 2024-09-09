from django.shortcuts import render, HttpResponse, redirect

def main(request):
    render(request,"productos.html")