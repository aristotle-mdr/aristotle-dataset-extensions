# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields
import ckeditor_uploader.fields
import aristotle_mdr.utils.migrations


class Migration(migrations.Migration):

    replaces = [('aristotle_dse', '0001_initial'), ('aristotle_dse', '0002_auto_20150510_0249'), ('aristotle_dse', '0003_add_clusters_improve_names'), ('aristotle_dse', '0004_auto_20160103_0200'), ('aristotle_dse', '0005_improve_inculsion_help_text'), ('aristotle_dse', '0006_auto_20160103_1855'), ('aristotle_dse', '0007_add_ordering_to_inclusions'), ('aristotle_dse', '0008_auto_20160318_2335'), ('aristotle_dse', '0009_auto_20160725_1958'), ('aristotle_dse', '0010_datasource_specification'), ('aristotle_dse', '0011_auto_20160726_2015'), ('aristotle_dse', '0012_fix_concept_fields')]

    dependencies = [
        ('aristotle_mdr', '0001_squashed_0017_add_organisations'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSetSpecification',
            fields=[
                ('_concept_ptr', models.OneToOneField(to='aristotle_mdr._concept', auto_created=True, primary_key=True, serialize=False, parent_link=True)),
                ('short_name', models.CharField(blank=True, max_length=100)),
                ('version', models.CharField(blank=True, max_length=20)),
                ('synonyms', models.CharField(blank=True, max_length=200)),
                ('references', ckeditor.fields.RichTextField(blank=True)),
                ('origin_URI', models.URLField(blank=True, help_text='If imported, the original location of the item')),
                ('comments', ckeditor.fields.RichTextField(blank=True, help_text='Descriptive comments about the metadata item.')),
                ('submitting_organisation', models.CharField(blank=True, max_length=256)),
                ('responsible_organisation', models.CharField(blank=True, max_length=256)),
                ('superseded_by', models.ForeignKey(to='aristotle_dse.DataSetSpecification', blank=True, related_name='supersedes', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('aristotle_mdr._concept',),
        ),
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('_concept_ptr', models.OneToOneField(to='aristotle_mdr._concept', auto_created=True, primary_key=True, serialize=False, parent_link=True)),
                ('short_name', models.CharField(blank=True, max_length=100)),
                ('version', models.CharField(blank=True, max_length=20)),
                ('synonyms', models.CharField(blank=True, max_length=200)),
                ('references', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('origin_URI', models.URLField(blank=True, help_text='If imported, the original location of the item')),
                ('comments', ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='Descriptive comments about the metadata item.')),
                ('submitting_organisation', models.CharField(blank=True, max_length=256)),
                ('responsible_organisation', models.CharField(blank=True, max_length=256)),
                ('linkToData', models.URLField(blank=True)),
                ('custodian', models.TextField(blank=True, max_length=256)),
                ('frequency', models.CharField(default='notStated', max_length=20, choices=[('annually', 'Annually'), ('biannually', 'Biannually'), ('quarterly', 'Quarterly'), ('monthly', 'Monthly'), ('adhoc', 'Ad hoc'), ('notStated', 'Not stated')])),
                ('superseded_by', models.ForeignKey(to='aristotle_dse.DataSource', blank=True, related_name='supersedes', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('aristotle_mdr._concept',),
        ),
        migrations.CreateModel(
            name='DSSDEInclusion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('maximum_occurances', models.PositiveIntegerField(default=1, help_text='The maximum number of times a item can be included in a dataset')),
                ('cardinality', models.CharField(default='conditional', max_length=20, choices=[('optional', 'Optional'), ('conditional', 'Conditional'), ('mandatory', 'Mandatory')], help_text='Specifies if a field is required, optional or conditional within a dataset based on this specification.')),
                ('specific_information', ckeditor.fields.RichTextField(blank=True, help_text='Any additional information on the inclusion of a data element or cluster in a dataset.')),
                ('conditional_obligation', models.TextField(blank=True, help_text='If an item is present conditionally, this field defines the conditions under which an item will appear.')),
                ('order', models.PositiveSmallIntegerField(blank=True, verbose_name='Position', help_text='If a dataset is ordered, this indicates which position this item is in a dataset.', null=True)),
                ('data_element', models.ForeignKey(related_name='dssInclusions', to='aristotle_mdr.DataElement')),
                ('dss', models.ForeignKey(to='aristotle_dse.DataSetSpecification')),
            ],
            options={
                'verbose_name': 'DSS Data Element Inclusion',
            },
        ),
        migrations.AddField(
            model_name='datasetspecification',
            name='ordered',
            field=models.BooleanField(default=False, help_text='Indiciates if the ordering for a dataset is must match exactly the order laid out in the specification.'),
        ),
        migrations.CreateModel(
            name='DSSClusterInclusion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('maximumOccurances', models.PositiveIntegerField(default=1)),
                ('cardinality', models.CharField(default='conditional', max_length=20, choices=[('optional', 'Optional'), ('conditional', 'Conditional'), ('mandatory', 'Mandatory')])),
                ('specificInformation', ckeditor.fields.RichTextField(blank=True)),
                ('conditionalObligation', models.TextField(blank=True)),
                ('order', models.PositiveSmallIntegerField(blank=True, verbose_name='Position', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='datasetspecification',
            name='collection_method',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True),
        ),
        migrations.AddField(
            model_name='datasetspecification',
            name='data_elements',
            field=models.ManyToManyField(to='aristotle_mdr.DataElement', blank=True, through='aristotle_dse.DSSDEInclusion', null=True),
        ),
        migrations.AddField(
            model_name='datasetspecification',
            name='implementation_end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='datasetspecification',
            name='implementation_start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='datasetspecification',
            name='statistical_unit',
            field=models.ForeignKey(to='aristotle_mdr._concept', blank=True, related_name='statistical_unit_of', help_text='Indiciates if the ordering for a dataset is must match exactly the order laid out in the specification.', null=True),
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
            field=models.ManyToManyField(to='aristotle_dse.DataSetSpecification', blank=True, through='aristotle_dse.DSSClusterInclusion', null=True),
        ),
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
        migrations.AlterField(
            model_name='dssclusterinclusion',
            name='cardinality',
            field=models.CharField(default='conditional', max_length=20, choices=[('optional', 'Optional'), ('conditional', 'Conditional'), ('mandatory', 'Mandatory')], help_text='Specifies if a field is required, optional or conditional within a dataset based on this specification.'),
        ),
        migrations.AlterField(
            model_name='dssclusterinclusion',
            name='conditional_obligation',
            field=models.TextField(blank=True, help_text='If an item is present conditionally, this field defines the conditions under which an item will appear.'),
        ),
        migrations.AlterField(
            model_name='dssclusterinclusion',
            name='maximum_occurances',
            field=models.PositiveIntegerField(default=1, help_text='The maximum number of times a item can be included in a dataset'),
        ),
        migrations.AlterField(
            model_name='dssclusterinclusion',
            name='order',
            field=models.PositiveSmallIntegerField(blank=True, verbose_name='Position', help_text='If a dataset is ordered, this indicates which position this item is in a dataset.', null=True),
        ),
        migrations.AlterField(
            model_name='dssclusterinclusion',
            name='specific_information',
            field=ckeditor.fields.RichTextField(blank=True, help_text='Any additional information on the inclusion of a data element or cluster in a dataset.'),
        ),
        migrations.AlterModelOptions(
            name='dssclusterinclusion',
            options={'verbose_name': 'DSS Cluster Inclusion'},
        ),
        migrations.AlterModelOptions(
            name='dssclusterinclusion',
            options={'ordering': ['order'], 'verbose_name': 'DSS Cluster Inclusion'},
        ),
        migrations.AlterModelOptions(
            name='dssdeinclusion',
            options={'ordering': ['order'], 'verbose_name': 'DSS Data Element Inclusion'},
        ),
        migrations.AlterField(
            model_name='datasetspecification',
            name='comments',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='Descriptive comments about the metadata item.'),
        ),
        migrations.AlterField(
            model_name='datasetspecification',
            name='references',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True),
        ),
        migrations.AlterField(
            model_name='dssclusterinclusion',
            name='specific_information',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='Any additional information on the inclusion of a data element or cluster in a dataset.'),
        ),
        migrations.AlterField(
            model_name='dssdeinclusion',
            name='specific_information',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='Any additional information on the inclusion of a data element or cluster in a dataset.'),
        ),
        migrations.AddField(
            model_name='datasource',
            name='specification',
            field=models.ForeignKey(to='aristotle_dse.DataSetSpecification', blank=True, help_text='The dataset specification to which this data source conforms', null=True),
        ),
        migrations.AlterField(
            model_name='datasource',
            name='frequency',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        aristotle_mdr.utils.migrations.MoveConceptFields(
            model_name='datasource',
        ),
        aristotle_mdr.utils.migrations.MoveConceptFields(
            model_name='datasetspecification',
        ),
        migrations.RemoveField(
            model_name='datasource',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='datasource',
            name='origin_URI',
        ),
        migrations.RemoveField(
            model_name='datasource',
            name='references',
        ),
        migrations.RemoveField(
            model_name='datasource',
            name='responsible_organisation',
        ),
        migrations.RemoveField(
            model_name='datasource',
            name='short_name',
        ),
        migrations.RemoveField(
            model_name='datasource',
            name='submitting_organisation',
        ),
        migrations.RemoveField(
            model_name='datasource',
            name='superseded_by',
        ),
        migrations.RemoveField(
            model_name='datasource',
            name='synonyms',
        ),
        migrations.RemoveField(
            model_name='datasource',
            name='version',
        ),
        migrations.RemoveField(
            model_name='datasetspecification',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='datasetspecification',
            name='origin_URI',
        ),
        migrations.RemoveField(
            model_name='datasetspecification',
            name='references',
        ),
        migrations.RemoveField(
            model_name='datasetspecification',
            name='responsible_organisation',
        ),
        migrations.RemoveField(
            model_name='datasetspecification',
            name='short_name',
        ),
        migrations.RemoveField(
            model_name='datasetspecification',
            name='submitting_organisation',
        ),
        migrations.RemoveField(
            model_name='datasetspecification',
            name='superseded_by',
        ),
        migrations.RemoveField(
            model_name='datasetspecification',
            name='synonyms',
        ),
        migrations.RemoveField(
            model_name='datasetspecification',
            name='version',
        ),
    ]
