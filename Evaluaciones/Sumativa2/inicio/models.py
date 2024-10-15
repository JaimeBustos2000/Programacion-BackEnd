from django.db import models

class Caracteristica(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=15)
    descripcion = models.TextField(max_length=200)

""""""
class Categoria(models.Model):

    CAT =[
        ("Tecnologia","Tecnologia"),
        ("Alimentos","Alimentos"),
        ("hogar","Hogar")
    ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20,choices=CAT)

    def __str__(self):
        return self.nombre


class Productos(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=7)
    nombre = models.CharField(max_length=22)
    precio = models.CharField(max_length=10)
    caracteristicas = models.ManyToManyField(Caracteristica)
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)




