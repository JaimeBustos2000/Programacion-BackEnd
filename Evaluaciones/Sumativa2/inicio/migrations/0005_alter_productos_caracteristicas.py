# Generated by Django 4.2.16 on 2024-10-14 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0004_alter_productos_caracteristicas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='caracteristicas',
            field=models.ManyToManyField(to='inicio.caracteristica'),
        ),
    ]
