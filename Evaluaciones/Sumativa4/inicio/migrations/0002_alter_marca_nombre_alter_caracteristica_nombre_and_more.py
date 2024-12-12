# Generated by Django 5.0.6 on 2024-12-10 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marca',
            name='nombre',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='caracteristica',
            name='nombre',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='nombre',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterModelOptions(
            name='caracteristica',
            options={},
        ),
        migrations.AlterModelOptions(
            name='categoria',
            options={},
        ),
        migrations.DeleteModel(
            name='NombreMarca',
        ),
        migrations.DeleteModel(
            name='OpcionCaracterisca',
        ),
        migrations.DeleteModel(
            name='OpcionCategoria',
        ),
    ]
