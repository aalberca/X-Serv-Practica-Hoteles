# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0002_remove_alojamiento_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seleccionados',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('usuario', models.CharField(max_length=32)),
                ('hota', models.TimeField(auto_now_add=True)),
                ('hotel_id', models.ForeignKey(to='MyApp.Alojamiento')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
