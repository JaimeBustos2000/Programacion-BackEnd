# Generated by Django 5.0.6 on 2024-10-15 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='nombre',
            field=models.CharField(choices=[('Frutas Y Verduras', 'Frutas y Verduras'), ('Carnes Y Pescados', 'Carnes y Pescados'), ('Lacteos Y Huevos', 'Lácteos y Huevos'), ('Panaderia Y Reposteria', 'Panadería y Repostería'), ('Cereales Y Granos', 'Cereales y Granos'), ('Bebidas', 'Bebidas'), ('Alimentos Congelados', 'Alimentos Congelados'), ('Snacks Y Botanas', 'Snacks y Botanas'), ('Comidas Preparadas', 'Comidas Preparadas'), ('Salsas Condimentos Y Especias', 'Salsas, Condimentos y Especias'), ('Alimentos Enlatados Y Conservas', 'Alimentos Enlatados y Conservas'), ('Productos Organicos', 'Productos Orgánicos'), ('Alimentos Sin Gluten', 'Alimentos Sin Gluten'), ('Dulces Y Chocolates', 'Dulces y Chocolates'), ('Aceites Y Grasas', 'Aceites y Grasas'), ('Pasta Y Arroces', 'Pasta y Arroces'), ('Legumbres', 'Legumbres')], max_length=31, unique=True),
        ),
    ]
