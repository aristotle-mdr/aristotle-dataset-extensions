from django.conf.urls import url
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _

from aristotle_dse import views, models
from aristotle_mdr import models as MDR

from aristotle_mdr.contrib.generic.views import (
    GenericAlterOneToManyView,
    GenericAlterManyToManyView
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
]
