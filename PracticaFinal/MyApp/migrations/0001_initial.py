# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alojamiento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('categoria', models.CharField(max_length=32)),
                ('subcategoria', models.CharField(max_length=32)),
                ('nombre', models.CharField(max_length=32)),
                ('descripcion', models.TextField()),
                ('web', models.CharField(max_length=200)),
                ('telefono', models.CharField(max_length=200)),
                ('direccion', models.CharField(max_length=200)),
                ('cod_postal', models.IntegerField()),
                ('email', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comentarios',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('texto', models.TextField()),
                ('usuario', models.CharField(max_length=32)),
                ('hotel_id', models.ForeignKey(to='MyApp.Alojamiento')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Imagenes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=132)),
                ('hotel', models.ForeignKey(to='MyApp.Alojamiento')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
