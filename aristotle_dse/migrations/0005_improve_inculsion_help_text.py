# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('aristotle_dse', '0004_auto_20160103_0200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dssclusterinclusion',
            name='cardinality',
            field=models.CharField(default='conditional', help_text='Specifies if a field is required, optional or conditional within a dataset based on this specification.', max_length=20, choices=[('optional', 'Optional'), ('conditional', 'Conditional'), ('mandatory', 'Mandatory')]),
        ),
        migrations.AlterField(
            model_name='dssclusterinclusion',
            name='conditional_obligation',
            field=models.TextField(help_text='If an item is present conditionally, this field defines the conditions under which an item will appear.', blank=True),
        ),
        migrations.AlterField(
            model_name='dssclusterinclusion',
            name='maximum_occurances',
            field=models.PositiveIntegerField(default=1, help_text='The maximum number of times a item can be included in a dataset'),
        ),
        migrations.AlterField(
            model_name='dssclusterinclusion',
            name='order',
            field=models.PositiveSmallIntegerField(help_text='If a dataset is ordered, this indicates which position this item is in a dataset.', null=True, verbose_name='Position', blank=True),
        ),
        migrations.AlterField(
            model_name='dssclusterinclusion',
            name='specific_information',
            field=ckeditor.fields.RichTextField(help_text='Any additional information on the inclusion of a data element or cluster in a dataset.', blank=True),
        ),
        migrations.AlterField(
            model_name='dssdeinclusion',
            name='cardinality',
            field=models.CharField(default='conditional', help_text='Specifies if a field is required, optional or conditional within a dataset based on this specification.', max_length=20, choices=[('optional', 'Optional'), ('conditional', 'Conditional'), ('mandatory', 'Mandatory')]),
        ),
        migrations.AlterField(
            model_name='dssdeinclusion',
            name='conditional_obligation',
            field=models.TextField(help_text='If an item is present conditionally, this field defines the conditions under which an item will appear.', blank=True),
        ),
        migrations.AlterField(
            model_name='dssdeinclusion',
            name='maximum_occurances',
            field=models.PositiveIntegerField(default=1, help_text='The maximum number of times a item can be included in a dataset'),
        ),
        migrations.AlterField(
            model_name='dssdeinclusion',
            name='order',
            field=models.PositiveSmallIntegerField(help_text='If a dataset is ordered, this indicates which position this item is in a dataset.', null=True, verbose_name='Position', blank=True),
        ),
        migrations.AlterField(
            model_name='dssdeinclusion',
            name='specific_information',
            field=ckeditor.fields.RichTextField(help_text='Any additional information on the inclusion of a data element or cluster in a dataset.', blank=True),
        ),
    ]
