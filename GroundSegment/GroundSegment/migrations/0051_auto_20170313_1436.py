# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-03-13 14:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0050_pasada_passgeneration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pasada',
            name='startTime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='pasada',
            name='stopTime',
            field=models.DateTimeField(),
        ),
    ]
