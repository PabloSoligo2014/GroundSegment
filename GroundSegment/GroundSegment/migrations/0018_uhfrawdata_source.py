# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-01 13:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0017_remove_tlmyvartype_sessionwrite'),
    ]

    operations = [
        migrations.AddField(
            model_name='uhfrawdata',
            name='source',
            field=models.CharField(default='simulation', help_text='Origen del dato, tipicamente cubesat/simulacion', max_length=24, verbose_name='Origen del dato, tipicamente cubesat/simulacion'),
        ),
    ]
