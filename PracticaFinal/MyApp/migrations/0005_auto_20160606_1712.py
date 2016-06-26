# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0004_auto_20160606_0826'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comentarios',
            old_name='hotel_id',
            new_name='hotel',
        ),
    ]
