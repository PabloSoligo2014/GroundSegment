# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-22 12:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0073_auto_20170816_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commandparameter',
            name='value',
            field=models.CharField(default='', max_length=1),
        ),
    ]