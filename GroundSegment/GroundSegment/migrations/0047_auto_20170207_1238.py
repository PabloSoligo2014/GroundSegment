# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-02-07 12:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0046_auto_20170207_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tmlyvar',
            name='tmlyVarType',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tmlyVars', to='GroundSegment.TlmyVarType'),
            preserve_default=False,
        ),
    ]