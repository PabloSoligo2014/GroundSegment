# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-02 13:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0018_uhfrawdata_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='tlmyvartype',
            name='position',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tlmyvartype',
            name='subPosition',
            field=models.IntegerField(default=0),
        ),
    ]
