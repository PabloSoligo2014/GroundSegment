# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-05 18:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alarm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField()),
                ('dtArrival', models.DateTimeField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='AlarmState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='Codigo del estado de la alarma', max_length=24, unique=True, verbose_name='Codigo del estado de la alarma')),
                ('description', models.CharField(help_text='Decripcion del estado de la alarma', max_length=100, unique=True, verbose_name='Decripcion del estado de la alarma')),
            ],
        ),
        migrations.CreateModel(
            name='AlarmType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='Codigo del satelite, ejemplo FS2017', max_length=24, unique=True, verbose_name='Codigo del tipo de alarma')),
                ('description', models.CharField(help_text='Decripcion del satelite', max_length=100, unique=True, verbose_name='Decripcion del tipo de alarma')),
                ('procedure', models.TextField(help_text='Procedimiento a ejecutar por los ingenieros de vuelo en caso de ocurrir alarma', max_length=512)),
                ('timeout', models.IntegerField(help_text='tiempo maximo para tratar la alarma', verbose_name='Tiempo maximo para tratar la alarma')),
            ],
        ),
        migrations.CreateModel(
            name='CommandType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='Codigo del tipo de comando', max_length=24, unique=True, verbose_name='Codigo del tipo de comando')),
                ('description', models.CharField(help_text='Decripcion del tipo de comando', max_length=100, unique=True, verbose_name='Decripcion del tipo de comando')),
                ('active', models.BooleanField(default=True)),
                ('transactional', models.BooleanField(default=False)),
                ('timeout', models.IntegerField(default=0, verbose_name='Tiempo en segundos?')),
                ('notes', models.TextField(max_length=512, null=True, verbose_name='Consecuencias, restricciones del comando')),
            ],
        ),
        migrations.CreateModel(
            name='CommandTypeParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Criticity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='Codigo del satelite, ejemplo FS2017', max_length=24, unique=True, verbose_name='Codigo de criticidad')),
                ('description', models.CharField(help_text='Decripcion del satelite', max_length=100, unique=True, verbose_name='Decripcion de la criticidad')),
                ('color', models.CharField(default='#FF0000', max_length=7)),
                ('sound', models.FileField(upload_to='', verbose_name='/media')),
            ],
            options={
                'verbose_name': 'Criticidad',
                'verbose_name_plural': 'Criticidades',
            },
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.CharField(help_text='Modulo donde normalmente se usuario el parametro', max_length=64, verbose_name='Modulo')),
                ('key', models.CharField(help_text='Clave', max_length=24, verbose_name='Clave')),
                ('value', models.CharField(help_text='Valor del parametro', max_length=128, verbose_name='Valor')),
                ('description', models.TextField(default='Describir parametro aqui', help_text='Descripcion del parametro, donde se usa, para que?', verbose_name='Descripcion')),
            ],
        ),
        migrations.CreateModel(
            name='Pass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('startTime', models.DateTimeField(auto_now_add=True)),
                ('stopTime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Propagation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('final', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PropagationDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('dt', models.DateTimeField()),
                ('positionX', models.FloatField()),
                ('positionY', models.FloatField()),
                ('positionZ', models.FloatField()),
                ('velocityX', models.FloatField()),
                ('velocityY', models.FloatField()),
                ('velocityZ', models.FloatField()),
                ('earthDistance', models.FloatField(default=0.0)),
                ('propagation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='propagationDetails', to='GroundSegment.Propagation')),
            ],
        ),
        migrations.CreateModel(
            name='Satellite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='Codigo del satelite, ejemplo FS2017', max_length=24, unique=True, verbose_name='Codigo del satelite')),
                ('description', models.CharField(help_text='Decripcion del satelite', max_length=100, unique=True, verbose_name='Decripcion del satelite')),
                ('noradId', models.IntegerField(help_text='Codigo norad del satelite', unique=True, verbose_name='Codigo norad del satelite')),
                ('active', models.BooleanField(default=True, verbose_name='Activacion/desactivacion del satelite')),
                ('notes', models.TextField(max_length=512, null=True, verbose_name='Observaciones sobre el satelite')),
            ],
        ),
        migrations.CreateModel(
            name='SatelliteState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='Codigo de estado del satelite', max_length=24, unique=True, verbose_name='Codigo de estado')),
                ('description', models.CharField(help_text='Decripcion del estado del satelite', max_length=100, unique=True, verbose_name='Codigo de estado')),
            ],
        ),
        migrations.CreateModel(
            name='Tle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tleDateTime', models.DateTimeField(auto_now_add=True)),
                ('downloaded', models.DateTimeField(auto_now_add=True)),
                ('lines', models.TextField(max_length=124)),
                ('satellite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tles', to='GroundSegment.Satellite')),
            ],
            options={
                'get_latest_by': 'tleDateTime',
            },
        ),
        migrations.AddField(
            model_name='satellite',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='satellites', to='GroundSegment.SatelliteState'),
        ),
        migrations.AddField(
            model_name='propagation',
            name='satellite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='propagations', to='GroundSegment.Satellite'),
        ),
        migrations.AddField(
            model_name='propagation',
            name='tle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='propagations', to='GroundSegment.Tle'),
        ),
        migrations.AddField(
            model_name='pass',
            name='satellite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pasadas', to='GroundSegment.Satellite'),
        ),
        migrations.AddField(
            model_name='commandtype',
            name='satellite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commandsType', to='GroundSegment.Satellite'),
        ),
        migrations.AddField(
            model_name='commandtype',
            name='satelliteStates',
            field=models.ManyToManyField(related_name='commandsType', to='GroundSegment.SatelliteState'),
        ),
        migrations.AddField(
            model_name='alarmtype',
            name='criticity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alarmstype', to='GroundSegment.Criticity'),
        ),
        migrations.AddField(
            model_name='alarm',
            name='alarmType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alarms', to='GroundSegment.AlarmType'),
        ),
        migrations.AddField(
            model_name='alarm',
            name='satellite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alarms', to='GroundSegment.Satellite'),
        ),
    ]
