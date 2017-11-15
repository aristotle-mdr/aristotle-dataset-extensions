from django.conf.urls import url
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _

from aristotle_dse import views, models
from aristotle_mdr import models as MDR

from aristotle_mdr.contrib.generic.views import (
    GenericAlterOneToManyView,
    GenericAlterManyToManyView,
)

urlpatterns = [

    url(r'^remove/deFromDss/(?P<de_id>\d+)/(?P<dss_id>\d+)', views.RemoveDEFromDSS.as_view(), name='removeDataElementFromDSS'),
    url(r'^remove/clusterFromDss/(?P<cluster_id>\d+)/(?P<dss_id>\d+)', views.RemoveClusterFromDSS.as_view(), name='removeClusterFromDSS'),

    url(r'^add/deToDss/(?P<dss_id>\d+)', views.addDataElementsToDSS, name='addDataElementsToDSS'),
    url(r'^add/clustersToDss/(?P<dss_id>\d+)', views.addClustersToDSS, name='addClustersToDSS'),

    url(r'^dss/edit_de_inclusion/(?P<dss_id>\d+)/(?P<de_id>\d+)', views.editDataElementInclusion, name='editDEInclusion'),
    url(r'^dss/edit_cluster_inclusion/(?P<dss_id>\d+)/(?P<cluster_id>\d+)', views.editClusterInclusion, name='editDSSInclusion'),
    url(r'^dss/reorder_inclusion/(?P<dss_id>\d+)/(?P<inc_type>\w+)', views.editInclusionOrder, name='editInclusionOrder'),

    # These are required for about pages to work. Include them, or custom items will die!
    url(r'^about/(?P<template>.+)/?$', views.DynamicTemplateView.as_view(), name="about"),
    url(r'^about/?$', TemplateView.as_view(template_name='aristotle_dse/static/about_aristotle_dse.html'), name="about"),

    # url(r'^add/column_to_distribution/(?P<dist_id>\d+)', views.add_column_to_distribution, name='add_column_to_distribution'),
    url(r'^add/column_to_distribution/(?P<iid>\d+)?/?$',
        GenericAlterOneToManyView.as_view(
            model_base=models.Distribution,
            model_to_add=models.DistributionDataElementPath,
            model_base_field='distributiondataelementpath_set',
            model_to_add_field='distribution',
            ordering_field='order',
            form_add_another_text=_('Add a column'),
            form_title=_('Change Columns')
        ), name='add_column_to_distribution'),

    url(r'^add/dataset_to_catalog/(?P<iid>\d+)?/?$',
        GenericAlterManyToManyView.as_view(
            model_base=models.DataCatalog,
            model_to_add=models.Dataset,
            model_base_field='dataset_set',
            form_title=_('Change Datasets')
        ), name='add_dataset_to_catalog'),

    url(r'^add/distribution_to_dataset/(?P<iid>\d+)?/?$',
        GenericAlterManyToManyView.as_view(
            model_base=models.Dataset,
            model_to_add=models.Distribution,
            model_base_field='distribution_set',
            form_title=_('Change Distributions')
        ), name='add_distribution_to_dataset'),

]
