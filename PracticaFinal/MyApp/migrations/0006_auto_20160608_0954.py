# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0005_auto_20160606_1712'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seleccionados',
            old_name='hotel_id',
            new_name='hotel',
        ),
        migrations.AddField(
            model_name='comentarios',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2016, 6, 8, 9, 54, 14, 82363, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
