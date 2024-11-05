# Generated by Django 5.0.6 on 2024-10-17 17:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NombreMarca',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='OpcionCaracterisca',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=25, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='OpcionCategoria',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=31, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='inicio.nombremarca')),
            ],
        ),
        migrations.CreateModel(
            name='Caracteristica',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.TextField(max_length=200)),
                ('nombre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.opcioncaracterisca')),
            ],
            options={
                'ordering': ['nombre__nombre'],
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='inicio.opcioncategoria')),
            ],
            options={
                'ordering': ['nombre__nombre'],
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('codigo', models.CharField(max_length=7, unique=True)),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('precio', models.IntegerField()),
                ('caracteristicas', models.ManyToManyField(max_length=50, to='inicio.caracteristica')),
                ('categoria', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='inicio.categoria')),
                ('marca', models.ForeignKey(default=1, max_length=50, on_delete=django.db.models.deletion.CASCADE, to='inicio.marca')),
            ],
        ),
    ]