# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-27 23:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0010_auto_20161127_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tlmyvartype',
            name='description',
            field=models.CharField(help_text='Decripcion del satelite', max_length=100, verbose_name='Decripcion del tipo de variable'),
        ),
    ]
