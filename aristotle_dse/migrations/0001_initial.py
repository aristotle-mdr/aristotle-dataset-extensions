# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('aristotle_mdr', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSetSpecification',
            fields=[
                ('_concept_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='aristotle_mdr._concept')),
                ('short_name', models.CharField(max_length=100, blank=True)),
                ('version', models.CharField(max_length=20, blank=True)),
                ('synonyms', models.CharField(max_length=200, blank=True)),
                ('references', ckeditor.fields.RichTextField(blank=True)),
                ('origin_URI', models.URLField(help_text='If imported, the original location of the item', blank=True)),
                ('comments', ckeditor.fields.RichTextField(help_text='Descriptive comments about the metadata item.', blank=True)),
                ('submitting_organisation', models.CharField(max_length=256, blank=True)),
                ('responsible_organisation', models.CharField(max_length=256, blank=True)),
                ('superseded_by', models.ForeignKey(related_name='supersedes', blank=True, to='aristotle_dse.DataSetSpecification', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('aristotle_mdr._concept',),
        ),
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('_concept_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='aristotle_mdr._concept')),
                ('short_name', models.CharField(max_length=100, blank=True)),
                ('version', models.CharField(max_length=20, blank=True)),
                ('synonyms', models.CharField(max_length=200, blank=True)),
                ('references', ckeditor.fields.RichTextField(blank=True)),
                ('origin_URI', models.URLField(help_text='If imported, the original location of the item', blank=True)),
                ('comments', ckeditor.fields.RichTextField(help_text='Descriptive comments about the metadata item.', blank=True)),
                ('submitting_organisation', models.CharField(max_length=256, blank=True)),
                ('responsible_organisation', models.CharField(max_length=256, blank=True)),
                ('linkToData', models.URLField(blank=True)),
                ('custodian', models.TextField(max_length=256, blank=True)),
                ('frequency', models.CharField(default='notStated', max_length=20, choices=[('annually', 'Annually'), ('biannually', 'Biannually'), ('quarterly', 'Quarterly'), ('monthly', 'Monthly'), ('adhoc', 'Ad hoc'), ('notStated', 'Not stated')])),
                ('superseded_by', models.ForeignKey(related_name='supersedes', blank=True, to='aristotle_dse.DataSource', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('aristotle_mdr._concept',),
        ),
        migrations.CreateModel(
            name='DSSDEInclusion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('maximumOccurances', models.PositiveIntegerField(default=1)),
                ('cardinality', models.CharField(default='conditional', max_length=20, choices=[('optional', 'Optional'), ('conditional', 'Conditional'), ('mandatory', 'Mandatory')])),
                ('specificInformation', ckeditor.fields.RichTextField(blank=True)),
                ('conditionalObligation', models.TextField(blank=True)),
                ('order', models.PositiveSmallIntegerField(null=True, verbose_name='Position', blank=True)),
                ('ordered', models.BooleanField(default=False)),
                ('dataElement', models.ForeignKey(related_name='dssInclusions', to='aristotle_mdr.DataElement')),
                ('dss', models.ForeignKey(related_name='dataElements', to='aristotle_dse.DataSetSpecification')),
            ],
            options={
                'verbose_name': 'DSS Data Element Inclusion',
            },
            bases=(models.Model,),
        ),
    ]
