# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0010_auto_20160622_1445'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modificaciones',
            name='titulo',
        ),
    ]
