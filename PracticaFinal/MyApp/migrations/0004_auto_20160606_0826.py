# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0003_seleccionados'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seleccionados',
            old_name='hota',
            new_name='hora',
        ),
    ]
