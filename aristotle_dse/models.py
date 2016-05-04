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
    """
    A collection of :model:`aristotle_mdr.DataElement`\s
    specifying the order and fields required for a standardised
    :model:`aristotle_dse.DataSource`.
    """
    edit_page_excludes = ['clusters','data_elements']
    template = "aristotle_dse/concepts/dataSetSpecification.html"
    ordered = models.BooleanField(
            default=False,
            help_text=_("Indiciates if the ordering for a dataset is must match exactly the order laid out in the specification.")
            )
    statistical_unit = models.ForeignKey(
            aristotle.models._concept,
            related_name='statistical_unit_of',
            blank=True,
            null=True,
            help_text=_("Indiciates if the ordering for a dataset is must match exactly the order laid out in the specification.")
            )
    data_elements = models.ManyToManyField(
            aristotle.models.DataElement,
            through='DSSDEInclusion'
            )
    clusters = models.ManyToManyField(
            'self',
            through='DSSClusterInclusion',
            symmetrical=False
            )
    collection_method = aristotle.models.RichTextField(
            blank=True,
            help_text=_('')
            )
    implementation_start_date = models.DateField(
            blank=True,
            null=True,
            help_text=_('')
            )
    implementation_end_date = models.DateField(
            blank=True,
            null=True,
            help_text=_('')
            )

    def addDataElement(self,data_element,**kwargs):
        inc = DSSDEInclusion.objects.get_or_create(
            data_element=data_element,
            dss = self,
            defaults = kwargs
            )

    def addCluster(self,child,**kwargs):
        inc = DSSClusterInclusion.objects.get_or_create(
            child=child,
            dss = self,
            defaults = kwargs
            )

    @property
    def registryCascadeItems(self):
        return list(self.clusters.all())+list(self.data_elements.all())

    def get_download_items(self):
        des = self.data_elements.all()
        return [
            (DataSetSpecification,self.clusters.all().order_by('name')),
            (aristotle.models.DataElement,des.order_by('name')),
            (aristotle.models.ObjectClass,aristotle.models.ObjectClass.objects.filter(dataelementconcept__dataelement__datasetspecification=self).order_by('name')),
            (aristotle.models.Property,aristotle.models.Property.objects.filter(dataelementconcept__dataelement__datasetspecification=self).order_by('name')),
            (aristotle.models.ValueDomain,aristotle.models.ValueDomain.objects.filter(dataelement__datasetspecification=self).order_by('name')),
        ]

class DSSInclusion(aristotle.models.aristotleComponent):
    class Meta:
        abstract=True
        ordering = ['order']
    @property
    def parentItem(self):
        return self.dss

    dss = models.ForeignKey(DataSetSpecification)
    maximum_occurances = models.PositiveIntegerField(
        default=1,
        help_text=_("The maximum number of times a item can be included in a dataset")
        )
    cardinality = models.CharField(
        choices=CARDINALITY, 
        default=CARDINALITY.conditional,
        max_length=20,
        help_text=_("Specifies if a field is required, optional or conditional within a dataset based on this specification.")
        )
    specific_information = RichTextField(
        blank=True,
        help_text=_("Any additional information on the inclusion of a data element or cluster in a dataset.")
        ) # may need to become HTML field.
    conditional_obligation = models.TextField(
        blank=True,
        help_text=_("If an item is present conditionally, this field defines the conditions under which an item will appear.")
        )
    order = models.PositiveSmallIntegerField(
        "Position",
        null=True,
        blank=True,
        help_text=_("If a dataset is ordered, this indicates which position this item is in a dataset.")
        )

# Holds the link between a DSS and a Data Element with the DSS Specific details.
class DSSDEInclusion(DSSInclusion):
    data_element = models.ForeignKey(aristotle.models.DataElement,related_name="dssInclusions")
    class Meta(DSSInclusion.Meta):
        verbose_name = "DSS Data Element Inclusion"

    @property
    def include(self):
        return self.data_element

# Holds the link between a DSS and a cluster with the DSS Specific details.
class DSSClusterInclusion(DSSInclusion):
    """
    The child in this relationship is considered to be a child of the parent DSS as specified by the `dss` property.
    """
    child = models.ForeignKey(DataSetSpecification,related_name='parent_dss')
    class Meta(DSSInclusion.Meta):
        verbose_name = "DSS Cluster Inclusion"
    
    @property
    def include(self):
        return self.child

def testData():
    pw,c = aristotle.models.Workgroup.objects.get_or_create(name="Possum Workgroup")
    de,c = aristotle.models.DataElement.objects.get_or_create(name="Person-sex, Code N",
            workgroup=pw,definition="The sex of the person with a code.",
            )

    dss,c = DataSetSpecification.objects.get_or_create(name="Person Dataset",
        workgroup=pw,definition="",
        )
    dss.addDataElement(de)

    dss_cluster,c = DataSetSpecification.objects.get_or_create(name="Person cluster",
        workgroup=pw,definition="",
        )
    de,c = aristotle.models.DataElement.objects.get_or_create(name="Person-Identifier, Code NNN",
            workgroup=pw,definition="The identifier for a person.",
            )
    dss_cluster.addDataElement(de)
    dss.addCluster(dss_cluster)