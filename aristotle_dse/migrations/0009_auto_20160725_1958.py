# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aristotle_dse', '0008_auto_20160318_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasetspecification',
            name='clusters',
            field=models.ManyToManyField(to='aristotle_dse.DataSetSpecification', null=True, through='aristotle_dse.DSSClusterInclusion', blank=True),
        ),
        migrations.AlterField(
            model_name='datasetspecification',
            name='data_elements',
            field=models.ManyToManyField(to='aristotle_mdr.DataElement', null=True, through='aristotle_dse.DSSDEInclusion', blank=True),
        ),
    ]
