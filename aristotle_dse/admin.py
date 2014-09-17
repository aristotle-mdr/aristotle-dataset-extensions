from django.contrib import admin
from aristotle_mdr import admin as aristotle_admin # Must include 'admin' directly, otherwise causes issues.
import aristotle_dse


class DataSourceAdmin(aristotle_admin.ConceptAdmin):
    fieldsets = aristotle_admin.ConceptAdmin.fieldsets + [
            ('Data Source',
                {'fields': ['linkToData','custodian','frequency',]}),
    ]

class DSSDEInclusionInline(admin.TabularInline):
    model=aristotle_dse.models.DSSDEInclusion
    extra=0
    classes = ('grp-collapse grp-closed',)
    raw_id_fields = ('dataElement',)
    autocomplete_lookup_fields = {
        'fk': ['dataElement']
    }

class DataSetSpecification(aristotle_admin.ConceptAdmin):
    inlines = aristotle_admin.ConceptAdmin.inlines + [DSSDEInclusionInline, ]

admin.site.register(aristotle_dse.models.DataSetSpecification,DataSetSpecification)
admin.site.register(aristotle_dse.models.DataSource,DataSourceAdmin)