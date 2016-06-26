# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0007_modificaciones'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seleccionados',
            name='hora',
        ),
        migrations.AddField(
            model_name='seleccionados',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2016, 6, 21, 21, 46, 52, 322740, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
