# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-08-15 16:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GroundSegment', '0065_commandtypeparameter_commandtype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tlmyvar',
            old_name='tmlyVarType',
            new_name='tlmyVarType',
        ),
    ]
