# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-01-30 13:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0033_auto_20170130_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tlmyvartype',
            name='frameType',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tlmyVarTypes', to='GroundSegment.FrameType'),
        ),
    ]