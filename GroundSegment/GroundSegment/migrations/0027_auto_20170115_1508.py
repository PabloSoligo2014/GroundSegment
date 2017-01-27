# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-01-15 15:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0026_delete_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitio',
            name='maskElev',
            field=models.FloatField(default=0.0, help_text='[grados]', verbose_name='Mascara de Elevacion'),
        ),
        migrations.AlterField(
            model_name='sitio',
            name='h',
            field=models.FloatField(help_text='[metros]', verbose_name='Altura'),
        ),
        migrations.AlterField(
            model_name='sitio',
            name='lat',
            field=models.FloatField(help_text='[Dato en Grados Decimales]', verbose_name='Latitud'),
        ),
        migrations.AlterField(
            model_name='sitio',
            name='lon',
            field=models.FloatField(help_text='[Grados Decimales]', verbose_name='Longitud'),
        ),
    ]