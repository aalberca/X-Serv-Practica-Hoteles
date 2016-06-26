# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0015_auto_20160625_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='megustas',
            name='usuario',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
    ]
