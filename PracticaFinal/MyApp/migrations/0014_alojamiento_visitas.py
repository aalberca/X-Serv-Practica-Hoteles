# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0013_auto_20160623_0912'),
    ]

    operations = [
        migrations.AddField(
            model_name='alojamiento',
            name='visitas',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
