# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_auto_20151211_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='ngreport',
            name='title',
            field=models.CharField(default=b'', max_length=500),
            preserve_default=True,
        ),
    ]
