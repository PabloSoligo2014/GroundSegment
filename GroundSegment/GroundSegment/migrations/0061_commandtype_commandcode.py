# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-01 16:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0060_auto_20170401_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='commandtype',
            name='commandCode',
            field=models.CharField(default='0', max_length=24, verbose_name='Codigo de comando segun el satelite, por ejemplo para isis cubesat telemetryEPS->23'),
        ),
    ]
