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
    def addDataElement(self,dataElement,**kwargs):
        inc = DSSDEInclusion.objects.get_or_create(
            dataElement=dataElement,
            dss = self,
            defaults = kwargs
            )

    @property
    def registryCascadeItems(self):
        return [i.dataElement for i in self.dataElements.all()]

    @property
    def getPdfItems(self):
        des = self.dataElements.all()
        return {
            'dataElements':(de.dataElement for de in des),
            'valueDomains':set(de.dataElement.valueDomain for de in des),
        }

# Holds the link between a DSS and a Data Element with the DSS Specific details.
class DSSDEInclusion(aristotle.models.aristotleComponent):
    dataElement = models.ForeignKey(aristotle.models.DataElement,related_name="dssInclusions")
    dss = models.ForeignKey(DataSetSpecification,related_name="dataElements")
    maximumOccurances = models.PositiveIntegerField(default=1)
    cardinality = models.CharField(choices=CARDINALITY, default=CARDINALITY.conditional,max_length=20)
    specificInformation = RichTextField(blank=True) # may need to become HTML field.
    conditionalObligation = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField("Position",null=True,blank=True)

    @property
    def parentItem(self):
        return self.dss

    class Meta:
        verbose_name = "DSS Data Element Inclusion"


def testData():
    pw,c = aristotle.models.Workgroup.objects.get_or_create(name="Possum Workgroup")
    de,c = aristotle.models.DataElement.objects.get_or_create(name="Person-sex, Code N",
            workgroup=pw,description="The sex of the person with a code.",
            )

    dss,c = DataSetSpecification.objects.get_or_create(name="Person Dataset",
        workgroup=pw,description="",
        )
    for de in aristotle.models.DataElement.objects.all():
        dss.addDataElement(de)
