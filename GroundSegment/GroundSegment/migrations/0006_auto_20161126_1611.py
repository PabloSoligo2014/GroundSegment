# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-26 19:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0005_auto_20161126_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tlmyvartype',
            name='lastCalSValue',
            field=models.CharField(blank=True, default=None, help_text='Valor como string de la variable de telemetria', max_length=24, null=True, verbose_name='Valor como string de la variable de telemetria'),
        ),
    ]
