# Generated by Django 5.0 on 2024-11-29 20:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0014_alter_auditoriaactividad_actividad_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipoactividad',
            name='programa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tipos_actividades', to='actividades.programa'),
        ),
    ]
