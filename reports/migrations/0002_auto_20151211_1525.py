# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ngreport',
            name='campaign',
        ),
        migrations.DeleteModel(
            name='Campaign',
        ),
    ]
