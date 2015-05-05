from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^', include('aristotle_mdr.urls')),
    url(r'^dse/', include('aristotle_dse.urls',app_name="aristotle_dse",namespace="aristotle_dse")),
    )