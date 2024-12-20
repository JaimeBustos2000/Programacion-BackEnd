# Generated by Django 5.0.6 on 2024-12-10 20:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0002_alter_marca_nombre_alter_caracteristica_nombre_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='NombreCaracteristica',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='caracteristica',
            name='nombre',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='inicio.nombrecaracteristica'),
        ),
    ]
