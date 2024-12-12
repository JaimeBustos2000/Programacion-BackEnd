from django.urls import path
from . import views

urlpatterns = [
    path('', views.validacion, name='validacion')
]