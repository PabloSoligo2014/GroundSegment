# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-15 16:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0068_remove_tlmyvar_tlmyvartype'),
    ]

    operations = [
        migrations.AddField(
            model_name='tlmyvar',
            name='tlmyVarType',
            field=models.ForeignKey(default=100001, on_delete=django.db.models.deletion.CASCADE, related_name='tlmyVars', to='GroundSegment.TlmyVarType'),
            preserve_default=False,
        ),
    ]
