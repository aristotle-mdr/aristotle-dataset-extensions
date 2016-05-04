# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor_uploader.fields


class Migration(migrations.Migration):

    dependencies = [
        ('aristotle_dse', '0007_add_ordering_to_inclusions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasetspecification',
            name='collection_method',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True),
        ),
        migrations.AlterField(
            model_name='datasetspecification',
            name='comments',
            field=ckeditor_uploader.fields.RichTextUploadingField(help_text='Descriptive comments about the metadata item.', blank=True),
        ),
        migrations.AlterField(
            model_name='datasetspecification',
            name='references',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True),
        ),
        migrations.AlterField(
            model_name='datasource',
            name='comments',
            field=ckeditor_uploader.fields.RichTextUploadingField(help_text='Descriptive comments about the metadata item.', blank=True),
        ),
        migrations.AlterField(
            model_name='datasource',
            name='references',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True),
        ),
        migrations.AlterField(
            model_name='dssclusterinclusion',
            name='specific_information',
            field=ckeditor_uploader.fields.RichTextUploadingField(help_text='Any additional information on the inclusion of a data element or cluster in a dataset.', blank=True),
        ),
        migrations.AlterField(
            model_name='dssdeinclusion',
            name='specific_information',
            field=ckeditor_uploader.fields.RichTextUploadingField(help_text='Any additional information on the inclusion of a data element or cluster in a dataset.', blank=True),
        ),
    ]
