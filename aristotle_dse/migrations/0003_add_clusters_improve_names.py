# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('aristotle_mdr', '0009_add_explicit_related_name_for_values'),
        ('aristotle_dse', '0002_auto_20150510_0249'),
    ]

    operations = [
        migrations.CreateModel(
            name='DSSClusterInclusion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('maximumOccurances', models.PositiveIntegerField(default=1)),
                ('cardinality', models.CharField(default='conditional', max_length=20, choices=[('optional', 'Optional'), ('conditional', 'Conditional'), ('mandatory', 'Mandatory')])),
                ('specificInformation', ckeditor.fields.RichTextField(blank=True)),
                ('conditionalObligation', models.TextField(blank=True)),
                ('order', models.PositiveSmallIntegerField(null=True, verbose_name='Position', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameField(
            model_name='dssdeinclusion',
            old_name='dataElement',
            new_name='data_element',
        ),
        migrations.AddField(
            model_name='datasetspecification',
            name='collection_method',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='datasetspecification',
            name='data_elements',
            field=models.ManyToManyField(to='aristotle_mdr.DataElement', through='aristotle_dse.DSSDEInclusion'),
        ),
        migrations.AddField(
            model_name='datasetspecification',
            name='implementation_end_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='datasetspecification',
            name='implementation_start_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='datasetspecification',
            name='statistical_unit',
            field=models.ForeignKey(related_name='statistical_unit_of', blank=True, to='aristotle_mdr._concept', help_text='Indiciates if the ordering for a dataset is must match exactly the order laid out in the specification.', null=True),
        ),
        migrations.AlterField(
            model_name='dssdeinclusion',
            name='dss',
            field=models.ForeignKey(to='aristotle_dse.DataSetSpecification'),
        ),
        migrations.AddField(
            model_name='dssclusterinclusion',
            name='child',
            field=models.ForeignKey(related_name='parent_dss', to='aristotle_dse.DataSetSpecification'),
        ),
        migrations.AddField(
            model_name='dssclusterinclusion',
            name='dss',
            field=models.ForeignKey(to='aristotle_dse.DataSetSpecification'),
        ),
        migrations.AddField(
            model_name='datasetspecification',
            name='clusters',
            field=models.ManyToManyField(to='aristotle_dse.DataSetSpecification', through='aristotle_dse.DSSClusterInclusion'),
        ),
    ]
