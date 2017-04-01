# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-03-27 12:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0053_auto_20170325_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='command',
            name='state',
            field=models.IntegerField(choices=[(0, 'Pending'), (1, 'Sent'), (2, 'Failed'), (3, 'Executed'), (4, 'Expirated')], default=0, max_length=1),
        ),
    ]