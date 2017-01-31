# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-01-31 20:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0038_auto_20170131_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='downlinkframe',
            name='ax25Destination',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='downlinkframe',
            name='ax25Protocol',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='downlinkframe',
            name='ax25Source',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='downlinkframe',
            name='frameTypeId',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='downlinkframe',
            name='packetNumber',
            field=models.IntegerField(default=0),
        ),
    ]