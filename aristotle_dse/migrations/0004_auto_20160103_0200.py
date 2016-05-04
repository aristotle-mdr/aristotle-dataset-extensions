# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aristotle_dse', '0003_add_clusters_improve_names'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dssclusterinclusion',
            old_name='conditionalObligation',
            new_name='conditional_obligation',
        ),
        migrations.RenameField(
            model_name='dssclusterinclusion',
            old_name='maximumOccurances',
            new_name='maximum_occurances',
        ),
        migrations.RenameField(
            model_name='dssclusterinclusion',
            old_name='specificInformation',
            new_name='specific_information',
        ),
        migrations.RenameField(
            model_name='dssdeinclusion',
            old_name='conditionalObligation',
            new_name='conditional_obligation',
        ),
        migrations.RenameField(
            model_name='dssdeinclusion',
            old_name='maximumOccurances',
            new_name='maximum_occurances',
        ),
        migrations.RenameField(
            model_name='dssdeinclusion',
            old_name='specificInformation',
            new_name='specific_information',
        ),
    ]
