# Generated by Django 5.0.6 on 2024-12-10 20:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0003_nombrecaracteristica_alter_caracteristica_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caracteristica',
            name='nombre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicio.nombrecaracteristica'),
        ),
    ]