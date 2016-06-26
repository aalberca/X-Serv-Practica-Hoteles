# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0014_alojamiento_visitas'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeGustas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('usuario', models.CharField(max_length=32)),
                ('hotel', models.ForeignKey(to='MyApp.Alojamiento')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='alojamiento',
            name='megustas',
        ),
    ]
