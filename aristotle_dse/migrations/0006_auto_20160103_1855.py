# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aristotle_dse', '0005_improve_inculsion_help_text'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dssclusterinclusion',
            options={'verbose_name': 'DSS Cluster Inclusion'},
        ),
    ]
