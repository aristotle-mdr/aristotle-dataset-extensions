import autocomplete_light
autocomplete_light.autodiscover()

from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from aristotle_dse import views

urlpatterns = patterns('aristotle_dse.views',
    url(r'^datasetspecification/(?P<iid>\d+)/?$', views.datasetspecification, name='dataSetSpecification'),
    url(r'^add/deToDss/(?P<dss_id>\d+)', views.addDataElementsToDSS, name='addDataElementsToDSS'),
    url(r'^add/clustersToDss/(?P<dss_id>\d+)', views.addClustersToDSS, name='addClustersToDSS'),
    url(r'^remove/deFromDss/(?P<de_id>\d+)/(?P<dss_id>\d+)', views.removeDataElementFromDSS, name='removeDataElementFromDSS'),
    url(r'^remove/clusterFromDss/(?P<cluster_id>\d+)/(?P<dss_id>\d+)', views.removeClusterFromDSS, name='removeClusterFromDSS'),

#These are required for about pages to work. Include them, or custom items will die!
    url(r'^about/(?P<template>.+)/?$', views.DynamicTemplateView.as_view(), name="about"),
    url(r'^about/?$', TemplateView.as_view(template_name='aristotle_dse/static/about_aristotle_dse.html'), name="about"),
)