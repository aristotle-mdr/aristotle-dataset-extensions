# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aristotle_dse', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dssdeinclusion',
            name='ordered',
        ),
        migrations.AddField(
            model_name='datasetspecification',
            name='ordered',
            field=models.BooleanField(default=False, help_text='Indiciates if the ordering for a dataset is must match exactly the order laid out in the specification.'),
            preserve_default=True,
        ),
    ]
