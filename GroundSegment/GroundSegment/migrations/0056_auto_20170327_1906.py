# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-03-27 19:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0055_auto_20170327_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='command',
            name='executedAt',
            field=models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='command',
            name='expiration',
            field=models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0, tzinfo=utc)),
        ),
    ]
