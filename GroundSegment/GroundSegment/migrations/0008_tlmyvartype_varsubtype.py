# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-26 21:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0007_auto_20161126_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='tlmyvartype',
            name='varSubType',
            field=models.IntegerField(choices=[(0, 'Direct'), (1, 'Derived')], default=0, verbose_name='Indica si es directa o derivada 0=Directa, 1=Derivada'),
        ),
    ]
