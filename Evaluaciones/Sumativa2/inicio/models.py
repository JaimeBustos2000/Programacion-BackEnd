from django.db import models

class OpcionCaracterisca(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.nombre

class OpcionCategoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=31, unique=True)

    def __str__(self):
        return self.nombre

class Caracteristica(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.ForeignKey(OpcionCaracterisca, on_delete=models.CASCADE)
    descripcion = models.TextField(max_length=200)

    class Meta:
        ordering = ['nombre__nombre']

    def __str__(self):
        return f"{self.nombre} - {self.descripcion}"

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.OneToOneField(OpcionCategoria, on_delete=models.CASCADE)

    class Meta:
        ordering = ['nombre__nombre']

    def __str__(self):
        return self.nombre.nombre
    
class NombreMarca(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Marca(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.OneToOneField(NombreMarca, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre.nombre

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=7, unique=True)
    marca = models.ForeignKey(Marca, max_length=50, on_delete=models.CASCADE, default=1)
    nombre = models.CharField(max_length=50,unique=True)
    precio = models.IntegerField(null=False,blank=False)
    caracteristicas = models.ManyToManyField(Caracteristica, max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.codigo