# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0011_remove_modificaciones_titulo'),
    ]

    operations = [
        migrations.AddField(
            model_name='modificaciones',
            name='titulo',
            field=models.CharField(default=b'Pagina', max_length=64),
            preserve_default=True,
        ),
    ]
