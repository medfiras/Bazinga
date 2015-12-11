# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_auto_20151211_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ngreport',
            name='activity',
        ),
        migrations.DeleteModel(
            name='Activity',
        ),
        migrations.RemoveField(
            model_name='ngreport',
            name='country',
        ),
        migrations.RemoveField(
            model_name='ngreport',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='ngreport',
            name='location',
        ),
        migrations.RemoveField(
            model_name='ngreport',
            name='longitude',
        ),
    ]
