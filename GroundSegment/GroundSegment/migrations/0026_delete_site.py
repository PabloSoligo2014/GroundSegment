# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-01-14 18:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0025_coefficient'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Site',
        ),
    ]
