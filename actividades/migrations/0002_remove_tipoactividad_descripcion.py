# Generated by Django 5.0 on 2024-11-05 23:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tipoactividad',
            name='descripcion',
        ),
    ]
