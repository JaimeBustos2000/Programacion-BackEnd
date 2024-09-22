from django.urls import path
from . import views

urlpatterns = [
    path('<str:codigo>/<str:nombre>/<str:marca>/<str:fechaven>/', views.validacion, name='validacion')
]