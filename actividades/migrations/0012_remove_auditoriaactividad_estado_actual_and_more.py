# Generated by Django 5.0 on 2024-11-28 02:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0011_alter_auditoriaactividad_accion_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auditoriaactividad',
            name='estado_actual',
        ),
        migrations.RemoveField(
            model_name='auditoriaactividad',
            name='estado_anterior',
        ),
    ]