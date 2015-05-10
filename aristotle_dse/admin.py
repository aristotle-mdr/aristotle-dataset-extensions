from django.contrib import admin
import aristotle_dse

from aristotle_mdr.register import register_concept

class DSSDEInclusionInline(admin.TabularInline):
    model=aristotle_dse.models.DSSDEInclusion
    extra=0
    classes = ('grp-collapse grp-closed',)
    raw_id_fields = ('dataElement',)
    autocomplete_lookup_fields = {
        'fk': ['dataElement']
    }

register_concept(aristotle_dse.models.DataSetSpecification,
    extra_fieldsets=[
            ('Ordering',
                {'fields': ['ordered',]}),
    ],
    extra_inlines=[DSSDEInclusionInline,])

register_concept(aristotle_dse.models.DataSource,
    extra_fieldsets=[
            ('Data Source',
                {'fields': ['linkToData','custodian','frequency',]}),
    ])