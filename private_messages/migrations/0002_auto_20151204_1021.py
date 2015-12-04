# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('private_messages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='purged_for_recipient',
            field=models.BooleanField(default=False, db_index=True, verbose_name='Purged for recipient'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='purged_for_sender',
            field=models.BooleanField(default=False, db_index=True, verbose_name='Purged for sender'),
            preserve_default=True,
        ),
    ]
