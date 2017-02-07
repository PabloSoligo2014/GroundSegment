# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-02-07 12:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0045_auto_20170206_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='commandtypeparameter',
            name='code',
            field=models.CharField(default='NoDet', help_text='Codigo del parametro', max_length=24, verbose_name='Codigo del parametro'),
        ),
        migrations.AddField(
            model_name='commandtypeparameter',
            name='description',
            field=models.CharField(default='NoDet', help_text='Decripcion del satelite', max_length=100, verbose_name='Decripcion del parametro'),
        ),
        migrations.AddField(
            model_name='tmlyvar',
            name='tmlyVarType',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tmlyVars', to='GroundSegment.TlmyVarType'),
        ),
    ]