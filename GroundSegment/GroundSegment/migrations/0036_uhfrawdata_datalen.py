# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-01-30 19:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0035_downlinkframe'),
    ]

    operations = [
        migrations.AddField(
            model_name='uhfrawdata',
            name='dataLen',
            field=models.IntegerField(default=0, verbose_name='Dimension del campo data, autoguardado'),
        ),
    ]
