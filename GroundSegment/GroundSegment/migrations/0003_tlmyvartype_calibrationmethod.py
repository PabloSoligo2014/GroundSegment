# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-26 18:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0002_auto_20161126_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='tlmyvartype',
            name='calibrationMethod',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tlmyVarTypes', to='GroundSegment.Calibration'),
        ),
    ]
