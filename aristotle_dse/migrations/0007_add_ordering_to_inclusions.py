# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aristotle_dse', '0006_auto_20160103_1855'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dssclusterinclusion',
            options={'ordering': ['order'], 'verbose_name': 'DSS Cluster Inclusion'},
        ),
        migrations.AlterModelOptions(
            name='dssdeinclusion',
            options={'ordering': ['order'], 'verbose_name': 'DSS Data Element Inclusion'},
        ),
    ]
