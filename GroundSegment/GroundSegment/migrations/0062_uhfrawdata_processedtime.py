# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-05-31 17:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0061_commandtype_commandcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='uhfrawdata',
            name='processedTime',
            field=models.FloatField(default=0.0, verbose_name='Tiempo en milisegundos que domoro en ser procesada'),
        ),
    ]
