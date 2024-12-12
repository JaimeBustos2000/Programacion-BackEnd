from django.db import models

class NombreCaracteristica(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.nombre}"

class Caracteristica(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.ForeignKey(NombreCaracteristica,on_delete=models.CASCADE)
    descripcion = models.TextField(max_length=200)

    def __str__(self):
        return f"{self.nombre} - {self.descripcion}"

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30,unique=True)

    def __str__(self):
        return self.nombre
    

class Marca(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=7, unique=True)
    marca = models.ForeignKey(Marca, max_length=50, on_delete=models.CASCADE, default=1)
    nombre = models.CharField(max_length=50, unique=True)
    precio = models.IntegerField(null=False, blank=False)
    caracteristicas = models.ManyToManyField(Caracteristica, max_length=50,related_name='productos')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default=1)

    def delete(self, *args, **kwargs):
        caracteristicas_a_eliminar = self.caracteristicas.all()
        
        # Eliminar las relaciones ManyToMany antes de eliminar el producto
        self.caracteristicas.clear()

        # Eliminar características si no están asociadas con otros productos
        for caracteristica in caracteristicas_a_eliminar:
            if not caracteristica.productos.exists(): 
                caracteristica.delete()

        # Eliminar el producto
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo} -{self.nombre}"
