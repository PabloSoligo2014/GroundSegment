# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-02 15:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0021_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='description',
            field=models.TextField(help_text='Decripcion del log', max_length=512, verbose_name='Decripcion log'),
        ),
    ]