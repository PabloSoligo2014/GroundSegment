# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-01 16:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0058_satellite_incontact'),
    ]

    operations = [
        migrations.AddField(
            model_name='command',
            name='binarycmb',
            field=models.BinaryField(null=True, verbose_name='Comando en formato binario listo para ser enviado por TCP/IP'),
        ),
    ]
