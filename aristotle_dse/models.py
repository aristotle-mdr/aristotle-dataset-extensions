from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _
from model_utils import Choices

import aristotle_mdr as aristotle
from aristotle_mdr.models import RichTextField
from aristotle_mdr.fields import ConceptForeignKey, ConceptManyToManyField


class DataCatalog(aristotle.models.concept):
    """
    A data catalog is a curated collection of metadata about datasets.
    """
    template = "aristotle_dse/concepts/datacatalog.html"
    issued = models.DateField(
        blank=True, null=True,
        help_text=_('Date of formal issuance (e.g., publication) of the catalog.'),
        )
    dct_modified = models.DateTimeField(
        blank=True, null=True,
        help_text=_('Most recent date on which the catalog was changed, updated or modified.'),
        )
    homepage = models.URLField(
        blank=True, null=True,
        help_text=_('The dataset specification to which this data source conforms'),
        )
    publisher = models.ForeignKey(
        aristotle.models.Organization,
        blank=True, null=True,
        help_text=_('The entity responsible for making the catalog online.'),
        )
    spatial = models.TextField(
        blank=True, null=True,
        help_text=_('The geographical area covered by the catalog.'),
        )
    license = models.TextField(
        blank=True, null=True,
        help_text=_(
            'This links to the license document under which the catalog is made available and not the datasets. '
            'Even if the license of the catalog applies to all of its datasets and distributions, '
            'it should be replicated on each distribution.'
        ),
        )

    @property
    def publishing_organisations(self):
        return aristotle.models.Organization.objects.filter(dataset__catalog=self).distinct()

    # @property
    # def homepage(self):
    #     return self.originURI


class Dataset(aristotle.models.concept):
    """
    A collection of data, published or curated by a single agent, and available
    for access or download in one or more formats.
    """
    template = "aristotle_dse/concepts/dataset.html"
    # Themes = slots with name 'theme'
    # Keywords = slots with name 'keyword'
    issued = models.DateField(
        blank=True, null=True,
        help_text=_('Date of formal issuance (e.g., publication) of the catalog.'),
        )
    publisher = models.ForeignKey(
        aristotle.models.Organization,
        blank=True, null=True,
        help_text=_('An entity responsible for making the dataset available.'),
        )
    accrual_periodicity = models.TextField(
        blank=True, null=True,
        help_text=_('The frequency at which dataset is published.'),
        )
    spatial = models.TextField(
        blank=True, null=True,
        help_text=_('Spatial coverage of the dataset.'),
        )
    temporal = models.TextField(
        blank=True, null=True,
        help_text=_('The temporal period that the dataset covers.'),
        )
    catalog = models.ForeignKey(
        DataCatalog,
        blank=True, null=True,
        help_text=_('An entity responsible for making the dataset available.'),
        )
    landing_page = models.URLField(
        blank=True, null=True,
        help_text=_('A Web page that can be navigated to in a Web browser to gain access to the dataset, its distributions and/or additional information'),
        )
    contact_point = models.TextField(
        blank=True, null=True,
        help_text=_('The temporal period that the dataset covers.'),
        )
    dct_modified = models.DateTimeField(
        blank=True, null=True,
        help_text=_('Most recent date on which the catalog was changed, updated or modified.'),
        )


class Distribution(aristotle.models.concept):
    """
    Represents a specific available form of a dataset.
    Each dataset might be available in different forms,
    these forms might represent different formats
    of the dataset or different endpoints.
    Examples of distributions include a downloadable CSV file, an API or an RSS feed
    """
    template = "aristotle_dse/concepts/distribution.html"
    serialize_weak_entities = [
        ('data_elements', 'distributiondataelementpath_set'),
    ]
    issued = models.DateField(
        blank=True, null=True,
        help_text=_('Date of formal issuance (e.g., publication) of the catalog.'),
        )
    dct_modified = models.DateTimeField(
        blank=True, null=True,
        help_text=_('Most recent date on which the catalog was changed, updated or modified.'),
        )
    dataset = models.ForeignKey(
        Dataset,
        blank=True, null=True,
        help_text=_('Connects a distribution to its available datasets'),
        )
    publisher = models.ForeignKey(
        aristotle.models.Organization,
        blank=True, null=True,
        help_text=_('An entity responsible for making the dataset available.'),
        )
    license = models.TextField(
        blank=True, null=True,
        help_text=_('This links to the license document under which the distribution is made available.'),
        )
    rights = models.TextField(
        blank=True, null=True,
        help_text=_('Information about rights held in and over the distribution.'),
        )
    access_URL = models.URLField(
        blank=True, null=True,
        help_text=_('A landing page, feed, SPARQL endpoint or other type of resource that gives access to the distribution of the dataset.'),
        )
    download_URL = models.URLField(
        blank=True, null=True,
        help_text=_('A file that contains the distribution of the dataset in a given format.'),
        )
    byte_size = models.TextField(  # Why text? Because CKAN returns ??? Maybe we can clean in the future
        blank=True, null=True,
        help_text=_('The size in bytes can be approximated when the precise size is not known.'),
        )
    media_type = models.CharField(
        blank=True, null=True,
        max_length=512,
        help_text=_('The media type of the distribution as defined by IANA.'),
        )
    format_type = models.CharField(  # renamed from format as python will complain
        blank=True, null=True,
        max_length=512,
        help_text=_('The file format of the distribution.'),
        )


class DistributionDataElementPath(aristotle.models.aristotleComponent):
    class Meta:
        ordering = ['order']

    @property
    def parentItem(self):
        return self.distribution

    distribution = models.ForeignKey(
        Distribution,
        blank=True, null=True,
        help_text=_('A relation to the DCAT Distribution Record.'),
        )
    data_element = ConceptForeignKey(
        aristotle.models.DataElement,
        blank=True, null=True,
        help_text=_('An entity responsible for making the dataset available.'),
        )
    logical_path = models.CharField(
        max_length=256,
        help_text=_("A text expression that specifies how to identify which series of data in the distribution maps to this data element")
        )
    order = models.PositiveSmallIntegerField(
        "Position",
        null=True, blank=True,
        help_text=_("Column position within a dataset.")
        )
    specialisation_classes = ConceptManyToManyField(
        aristotle.models.ObjectClass,
        help_text=_(""),
        blank=True
    )


CARDINALITY = Choices(('optional', _('Optional')), ('conditional', _('Conditional')), ('mandatory', _('Mandatory')))


class DataSetSpecification(aristotle.models.concept):
    """
    A collection of :model:`aristotle_mdr.DataElement`\s
    specifying the order and fields required for a standardised
    :model:`aristotle_dse.DataSource`.
    """
    edit_page_excludes = ['clusters', 'data_elements']
    serialize_weak_entities = [
        ('clusters', 'dssclusterinclusion_set'),
        ('data_elements', 'dssdeinclusion_set'),
    ]

    template = "aristotle_dse/concepts/dataSetSpecification.html"
    ordered = models.BooleanField(
        default=False,
        help_text=_("Indicates if the ordering for a dataset is must match exactly the order laid out in the specification.")
        )
    statistical_unit = ConceptForeignKey(
        aristotle.models._concept,
        related_name='statistical_unit_of',
        blank=True,
        null=True,
        help_text=_("Indiciates if the ordering for a dataset is must match exactly the order laid out in the specification.")
        )
    data_elements = ConceptManyToManyField(
        aristotle.models.DataElement,
        blank=True,
        through='DSSDEInclusion'
        )
    clusters = ConceptManyToManyField(
        'self',
        through='DSSClusterInclusion',
        blank=True,
        null=True,
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

    def addDataElement(self, data_element, **kwargs):
        inc = DSSDEInclusion.objects.get_or_create(
            data_element=data_element,
            dss=self,
            defaults=kwargs
            )

    def addCluster(self, child, **kwargs):
        inc = DSSClusterInclusion.objects.get_or_create(
            child=child,
            dss=self,
            defaults=kwargs
            )

    @property
    def registry_cascade_items(self):
        return list(self.clusters.all()) + list(self.data_elements.all())

    def get_download_items(self):
        return [
            (DataSetSpecification, self.clusters.all()),
            (aristotle.models.DataElement, self.data_elements.all()),
            (
                aristotle.models.ObjectClass,
                aristotle.models.ObjectClass.objects.filter(dataelementconcept__dataelement__datasetspecification=self)
            ),
            (
                aristotle.models.Property,
                aristotle.models.Property.objects.filter(dataelementconcept__dataelement__datasetspecification=self)
            ),
            (
                aristotle.models.ValueDomain,
                aristotle.models.ValueDomain.objects.filter(dataelement__datasetspecification=self)
            ),
        ]


class DSSInclusion(aristotle.models.aristotleComponent):
    class Meta:
        abstract=True
        ordering = ['order']

    @property
    def parentItem(self):
        return self.dss

    dss = ConceptForeignKey(DataSetSpecification)
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
        )  # may need to become HTML field.
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
    data_element = ConceptForeignKey(aristotle.models.DataElement, related_name="dssInclusions")
    specialisation_classes = ConceptManyToManyField(
        aristotle.models.ObjectClass,
        help_text=_("")
    )

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
    child = ConceptForeignKey(DataSetSpecification, related_name='parent_dss')

    class Meta(DSSInclusion.Meta):
        verbose_name = "DSS Cluster Inclusion"

    @property
    def include(self):
        return self.child
