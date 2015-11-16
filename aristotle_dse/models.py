from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _
from model_utils import Choices

import aristotle_mdr as aristotle
from aristotle_mdr.models import RichTextField

FREQUENCY = Choices( ('annually', _('Annually')),
        ('biannually', _('Biannually')),
        ('quarterly', _('Quarterly')),
        ('monthly', _('Monthly')),
        ('adhoc', _('Ad hoc')),
        ('notStated', _('Not stated')),
    )

class DataSource(aristotle.models.concept):
    template = "aristotle_dse/concepts/dataSource.html"
    #qualityStatement = models.ForeignKey(QualityStatement,blank=True,null=True)
    linkToData = models.URLField(blank=True)
    custodian = models.TextField(max_length=256,blank=True)
    frequency = models.CharField(choices=FREQUENCY,default=FREQUENCY.notStated,max_length=20)


CARDINALITY = Choices(('optional', _('Optional')),('conditional', _('Conditional')), ('mandatory', _('Mandatory')))
class DataSetSpecification(aristotle.models.concept):
    template = "aristotle_dse/concepts/dataSetSpecification.html"
    ordered = models.BooleanField(default=False,help_text=_("Indiciates if the ordering for a dataset is must match exactly the order laid out in the specification."))
    statistical_unit = models.ForeignKey(aristotle.models.concept,blank=True,null=True,help_text=_("Indiciates if the ordering for a dataset is must match exactly the order laid out in the specification."))
    data_elements = models.ManyToManyField(aristotle.models.DataElement,through='DSSDEInclusion')
    clusters = models.ManyToManyField('self',through='DSSClusterInclusion')
    collection_method = aristotle.models.RichTextField(blank=True,help_text=_(''))
    implementation_start_date = models.DateField(blank=True,null=True,
            help_text=_(''))
    implementation_end_date = models.DateField(blank=True,null=True,
            help_text=_(''))

    def addDataElement(self,dataElement,**kwargs):
        inc = DSSDEInclusion.objects.get_or_create(
            dataElement=dataElement,
            dss = self,
            defaults = kwargs
            )

    @property
    def registryCascadeItems(self):
        return list(self.clusters.all())+list(self.data_elements.all())

    @property
    def getPdfItems(self):
        des = self.data_elements.all()
        return {
            'dataElements':des,
            'valueDomains':set(de.valueDomain for de in des),
        }

class DSSInclusion(aristotle.models.aristotleComponent):
    class Meta:
        abstract=True
    @property
    def parentItem(self):
        return self.dss

    dss = models.ForeignKey(DataSetSpecification)
    maximumOccurances = models.PositiveIntegerField(default=1)
    cardinality = models.CharField(choices=CARDINALITY, default=CARDINALITY.conditional,max_length=20)
    specificInformation = RichTextField(blank=True) # may need to become HTML field.
    conditionalObligation = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField("Position",null=True,blank=True)

# Holds the link between a DSS and a Data Element with the DSS Specific details.
class DSSDEInclusion(DSSInclusion):
    data_element = models.ForeignKey(aristotle.models.DataElement,related_name="dssInclusions")
    class Meta:
        verbose_name = "DSS Data Element Inclusion"

# Holds the link between a DSS and a cluster with the DSS Specific details.
class DSSClusterInclusion(DSSInclusion):
    child = models.ForeignKey(DataSetSpecification)


def testData():
    pw,c = aristotle.models.Workgroup.objects.get_or_create(name="Possum Workgroup")
    de,c = aristotle.models.DataElement.objects.get_or_create(name="Person-sex, Code N",
            workgroup=pw,definition="The sex of the person with a code.",
            )

    dss,c = DataSetSpecification.objects.get_or_create(name="Person Dataset",
        workgroup=pw,definition="",
        )
    for de in aristotle.models.DataElement.objects.all():
        dss.addDataElement(de)
