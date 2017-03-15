# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aristotle_mdr', '0017_add_organisations'),
        ('aristotle_mdr_identifiers', '0001_initial'),
        ('aristotle_dse', '0012_fix_concept_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataCatalog',
            fields=[
                ('_concept_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='aristotle_mdr._concept')),
                ('issued', models.DateField(help_text='Date of formal issuance (e.g., publication) of the catalog.', null=True, blank=True)),
                ('dct_modified', models.DateTimeField(help_text='Most recent date on which the catalog was changed, updated or modified.', null=True, blank=True)),
                ('homepage', models.URLField(help_text='The dataset specification to which this data source conforms', null=True, blank=True)),
                ('spatial', models.TextField(help_text='The geographical area covered by the catalog.', null=True, blank=True)),
                ('license', models.TextField(help_text='This links to the license document under which the catalog is made available and not the datasets. Even if the license of the catalog applies to all of its datasets and distributions, it should be replicated on each distribution.', null=True, blank=True)),
                ('publisher', models.ForeignKey(blank=True, to='aristotle_mdr.Organization', help_text='The entity responsible for making the catalog online.', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('aristotle_mdr._concept',),
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('_concept_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='aristotle_mdr._concept')),
                ('issued', models.DateField(help_text='Date of formal issuance (e.g., publication) of the catalog.', null=True, blank=True)),
                ('accrual_periodicity', models.TextField(help_text='\tThe frequency at which dataset is published.', null=True, blank=True)),
                ('spatial', models.TextField(help_text='Spatial coverage of the dataset.', null=True, blank=True)),
                ('temporal', models.TextField(help_text='The temporal period that the dataset covers.', null=True, blank=True)),
                ('landing_page', models.URLField(help_text='A Web page that can be navigated to in a Web browser to gain access to the dataset, its distributions and/or additional information', null=True, blank=True)),
                ('contact_point', models.TextField(help_text='The temporal period that the dataset covers.', null=True, blank=True)),
                ('dct_modified', models.DateTimeField(help_text='Most recent date on which the catalog was changed, updated or modified.', null=True, blank=True)),
                ('catalog', models.ForeignKey(blank=True, to='aristotle_dse.DataCatalog', help_text='An entity responsible for making the dataset available.', null=True)),
                ('publisher', models.ForeignKey(blank=True, to='aristotle_mdr.Organization', help_text='An entity responsible for making the dataset available.', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('aristotle_mdr._concept',),
        ),
        migrations.CreateModel(
            name='Distribution',
            fields=[
                ('_concept_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='aristotle_mdr._concept')),
                ('issued', models.DateField(help_text='Date of formal issuance (e.g., publication) of the catalog.', null=True, blank=True)),
                ('dct_modified', models.DateTimeField(help_text='Most recent date on which the catalog was changed, updated or modified.', null=True, blank=True)),
                ('license', models.TextField(help_text='This links to the license document under which the distribution is made available.', null=True, blank=True)),
                ('rights', models.TextField(help_text='Information about rights held in and over the distribution.', null=True, blank=True)),
                ('access_URL', models.URLField(help_text='A landing page, feed, SPARQL endpoint or other type of resource that gives access to the distribution of the dataset.', null=True, blank=True)),
                ('download_URL', models.URLField(help_text='A file that contains the distribution of the dataset in a given format.', null=True, blank=True)),
                ('byte_size', models.TextField(help_text='The size in bytes can be approximated when the precise size is not known.')),
                ('media_type', models.CharField(help_text='The media type of the distribution as defined by IANA.', max_length=512)),
                ('format_type', models.CharField(help_text='The file format of the distribution.', max_length=512)),
                ('publisher', models.ForeignKey(blank=True, to='aristotle_mdr.Organization', help_text='An entity responsible for making the dataset available.', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('aristotle_mdr._concept',),
        ),
        migrations.CreateModel(
            name='DistributionDataElementPath',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('logical_path', models.CharField(help_text='A text expression that specifies how to identify which series of data in the distribution maps to this data element', max_length=256)),
                ('order', models.PositiveSmallIntegerField(help_text='Column position within a dataset.', null=True, verbose_name='Position', blank=True)),
                ('data_element', models.ForeignKey(blank=True, to='aristotle_mdr.DataElement', help_text='An entity responsible for making the dataset available.', null=True)),
                ('distribution', models.ForeignKey(blank=True, to='aristotle_dse.Distribution', help_text='A relation to the DCAT Distribution Record.', null=True)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.RemoveField(
            model_name='datasource',
            name='_concept_ptr',
        ),
        migrations.RemoveField(
            model_name='datasource',
            name='specification',
        ),
        migrations.AlterField(
            model_name='datasetspecification',
            name='ordered',
            field=models.BooleanField(default=False, help_text='Indicates if the ordering for a dataset is must match exactly the order laid out in the specification.'),
        ),
        migrations.DeleteModel(
            name='DataSource',
        ),
        migrations.AddField(
            model_name='distribution',
            name='specification',
            field=models.ForeignKey(blank=True, to='aristotle_dse.DataSetSpecification', help_text='The dataset specification to which this data source conforms', null=True),
        ),
        migrations.AddField(
            model_name='distribution',
            name='dataset',
            field=models.ForeignKey(blank=True, to='aristotle_dse.Dataset', help_text='Connects a distribution to its available datasets', null=True),
        ),
    ]
