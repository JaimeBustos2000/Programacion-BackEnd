from django.urls import path
from . import views

urlpatterns = [
    path('<str:codigo>/', views.validacion, name='validacion')
]