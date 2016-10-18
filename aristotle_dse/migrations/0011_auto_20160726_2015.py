# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aristotle_dse', '0010_datasource_specification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasource',
            name='frequency',
            field=models.CharField(max_length=512, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='datasource',
            name='specification',
            field=models.ForeignKey(blank=True, to='aristotle_dse.DataSetSpecification', help_text='The dataset specification to which this data source conforms', null=True),
        ),
    ]
