# Generated by Django 5.0 on 2024-11-06 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0003_evidencia_archivo_evidencia_enlace'),
    ]

    operations = [
        migrations.AlterField(
            model_name='informe',
            name='fecha_fin',
            field=models.DateField(default=''),
        ),
        migrations.AlterField(
            model_name='informe',
            name='fecha_inicio',
            field=models.DateField(default=''),
        ),
    ]
