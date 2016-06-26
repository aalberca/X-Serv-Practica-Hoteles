# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0012_modificaciones_titulo'),
    ]

    operations = [
        migrations.AddField(
            model_name='alojamiento',
            name='megustas',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='modificaciones',
            name='titulo',
            field=models.CharField(default=b'', max_length=64),
            preserve_default=True,
        ),
    ]
