# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aristotle_dse', '0009_auto_20160725_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasource',
            name='specification',
            field=models.ForeignKey(blank=True, to='aristotle_dse.DataSetSpecification', null=True),
        ),
    ]
