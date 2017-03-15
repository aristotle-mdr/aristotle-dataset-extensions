from django.conf.urls import include, url

urlpatterns = [
    url(r'^', include('aristotle_mdr.urls')),
    url(r'^dse/', include('aristotle_dse.urls',app_name="aristotle_dse",namespace="aristotle_dse")),
]