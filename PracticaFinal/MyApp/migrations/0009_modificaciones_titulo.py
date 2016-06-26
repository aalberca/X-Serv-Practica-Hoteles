# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0008_auto_20160621_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='modificaciones',
            name='titulo',
            field=models.CharField(default=datetime.datetime(2016, 6, 22, 14, 40, 18, 242978, tzinfo=utc), max_length=64),
            preserve_default=False,
        ),
    ]
