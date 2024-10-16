from django.db import models

class Caracteristica(models.Model):
    CARACTERISTICAS = [
        ("Color","Color"),
        ("Cantidad","Cantidad"),
        ("Tamaño","Tamaño"),
        ("Peso en Kg","Peso en Kg"),
        ("Vencimiento","Vencimiento"),
        ("Origen","Origen"),
        ("Otros","Otros"),
        ]
    
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25,choices=CARACTERISTICAS)
    descripcion = models.TextField(max_length=200)

    def __str__(self):
        return f"{self.nombre} - {self.descripcion}"

class Categoria(models.Model):
    CATEGORIAS_ALIMENTOS = [
        ("Frutas Y Verduras", "Frutas y Verduras"),
        ("Carnes Y Pescados", "Carnes y Pescados"),
        ("Lacteos Y Huevos", "Lácteos y Huevos"),
        ("Panaderia Y Reposteria", "Panadería y Repostería"),
        ("Cereales Y Granos", "Cereales y Granos"),
        ("Bebidas", "Bebidas"),
        ("Alimentos Congelados", "Alimentos Congelados"),
        ("Snacks Y Botanas", "Snacks y Botanas"),
        ("Comidas Preparadas", "Comidas Preparadas"),
        ("Salsas Condimentos Y Especias", "Salsas, Condimentos y Especias"),
        ("Alimentos Enlatados Y Conservas", "Alimentos Enlatados y Conservas"),
        ("Productos Organicos", "Productos Orgánicos"),
        ("Alimentos Sin Gluten", "Alimentos Sin Gluten"),
        ("Dulces Y Chocolates", "Dulces y Chocolates"),
        ("Aceites Y Grasas", "Aceites y Grasas"),
        ("Pasta Y Arroces", "Pasta y Arroces"),
        ("Legumbres", "Legumbres"),
    ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=31,choices=CATEGORIAS_ALIMENTOS,unique=True,null=False)

    def __str__(self):
        return self.nombre


class Marca(models.Model):
    
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=7,unique=True)
    marca = models.ForeignKey(Marca,max_length=50,on_delete=models.CASCADE,default=1)
    nombre = models.CharField(max_length=50)
    precio = models.CharField(max_length=10)
    caracteristicas = models.ManyToManyField(Caracteristica,max_length=50)
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.codigo