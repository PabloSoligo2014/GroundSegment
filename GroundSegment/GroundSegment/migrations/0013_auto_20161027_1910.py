# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-27 19:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0012_auto_20160928_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarm',
            name='dtArrival',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
