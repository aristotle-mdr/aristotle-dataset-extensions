from django.contrib import admin
import aristotle_dse

from aristotle_mdr.register import register_concept

class DSSDEInclusionInline(admin.TabularInline):
    model=aristotle_dse.models.DSSDEInclusion
    extra=0
    classes = ('grp-collapse grp-closed',)
    raw_id_fields = ('data_element',)
    autocomplete_lookup_fields = {
        'fk': ['data_element']
    }
class DSSClusterInclusionInline(admin.TabularInline):
    model=aristotle_dse.models.DSSClusterInclusion
    extra=0
    classes = ('grp-collapse grp-closed',)
    fk_name = 'dss'
    raw_id_fields = ('child',)
    autocomplete_lookup_fields = {
        'fk': ['child']
    }

register_concept(aristotle_dse.models.DataSetSpecification,
    extra_fieldsets=[
        ('Methodology',
            {'fields': ['statistical_unit',
                        'collection_method',
                        'ordered',
                        ('implementation_start_date','implementation_end_date'),
                        ]}
        ),
    ],
    extra_inlines=[DSSDEInclusionInline,DSSClusterInclusionInline],
    reversion = {
        'follow': ['dssdeinclusion_set','dssclusterinclusion_set'],
        'follow_classes':[aristotle_dse.models.DSSClusterInclusion,aristotle_dse.models.DSSDEInclusion]
        },
    )

register_concept(aristotle_dse.models.DataSource,
    extra_fieldsets=[
            ('Data Source',
                {'fields': ['linkToData','custodian','frequency',]}),
    ])