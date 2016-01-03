﻿from aristotle_mdr.perms import user_can_view, user_can_edit, user_in_workgroup, user_is_workgroup_manager, user_can_change_status

from django.shortcuts import render, get_object_or_404
import aristotle_mdr as aristotle
import aristotle_dse
from aristotle_dse import forms

from django.views.generic import TemplateView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def datasetspecification(*args,**kwargs):
    return aristotle.views.render_if_user_can_view(aristotle_dse.models.DataSetSpecification,*args,**kwargs)

def datasource(*args,**kwargs):
    return aristotle.views.render_if_user_can_view(aristotle_dse.models.DataSource,*args,**kwargs)

def addDataElementsToDSS(request,dss_id):
    dss = get_object_or_404(aristotle_dse.models.DataSetSpecification,id=dss_id)
    if not user_can_edit(request.user,dss):
        raise PermissionDenied
    qs=aristotle.models.DataElement.objects.filter().visible(request.user)
    if request.method == 'POST': # If the form has been submitted...
        form = forms.AddDataElementsToDSSForm(request.POST,user=request.user,qs=qs,dss=dss) # A form bound to the POST data
        if form.is_valid():
            cardinality = form.cleaned_data['cardinality']
            maxOccurs = form.cleaned_data['maximum_occurances']
            for de in form.cleaned_data['dataElements']:
                dss.addDataElement(data_element=de,
                    maximumOccurances=maxOccurs,
                    cardinality=cardinality
                )
            return HttpResponseRedirect(reverse("aristotle_dse:dataSetSpecification",args=[dss.id]))
    else:
        form = forms.AddDataElementsToDSSForm(user=request.user,qs=qs,dss=dss)

    return render(request,"aristotle_dse/actions/addDataElementsToDSS.html",
            {"item":dss,
             "form":form,
                }
            )

def addClustersToDSS(request,dss_id):
    dss = get_object_or_404(aristotle_dse.models.DataSetSpecification,id=dss_id)
    if not user_can_edit(request.user,dss):
        raise PermissionDenied
    qs=aristotle_dse.models.DataSetSpecification.objects.filter().visible(request.user)
    if request.method == 'POST': # If the form has been submitted...
        form = forms.AddClustersToDSSForm(request.POST,user=request.user,qs=qs,dss=dss) # A form bound to the POST data
        if form.is_valid():
            cardinality = form.cleaned_data['cardinality']
            maxOccurs = form.cleaned_data['maximum_occurances']
            for dss in form.cleaned_data['clusters']:
                dss.addCluster(child=dss,
                    maximumOccurances=maxOccurs,
                    cardinality=cardinality
                )
            return HttpResponseRedirect(reverse("aristotle_dse:dataSetSpecification",args=[dss.id]))
    else:
        form = forms.AddClustersToDSSForm(user=request.user,qs=qs,dss=dss)

    return render(request,"aristotle_dse/actions/addClustersToDSS.html",
            {"item":dss,
             "form":form,
                }
            )

def removeClusterFromDSS(request,cluster_id,dss_id):
    cluster = get_object_or_404(aristotle_dse.models.DataSetSpecification,id=cluster_id)
    dss = get_object_or_404(aristotle_dse.models.DataSetSpecification,id=dss_id)
    if user_can_view(request.user,cluster) and user_can_edit(request.user,dss):
        dss.dssclusterinclusion_set.filter(child=cluster).delete()
    else:
        raise PermissionDenied
    return HttpResponseRedirect(dss.get_absolute_url())

def removeDataElementFromDSS(request,de_id,dss_id):
    de = get_object_or_404(aristotle.models.DataElement,id=de_id)
    dss = get_object_or_404(aristotle_dse.models.DataSetSpecification,id=dss_id)
    if user_can_view(request.user,de) and user_can_edit(request.user,dss):
        dss.dssdeinclusion_set.filter(data_element=de).delete()
    else:
        raise PermissionDenied
    return HttpResponseRedirect(dss.get_absolute_url())

def editDataElementInclusion(request,dss_id,de_id):
    dss = get_object_or_404(aristotle_dse.models.DataSetSpecification,id=dss_id)
    de=get_object_or_404(aristotle.models.DataElement,id=de_id)
    if not (user_can_edit(request.user,dss) and user_can_view(request.user,de)):
        raise PermissionDenied
    inclusion = get_object_or_404(aristotle_dse.models.DSSDEInclusion,data_element = de,dss = dss)


    if request.method == 'POST': # If the form has been submitted...
        form = forms.EditDataElementInclusionForm(request.POST,instance=inclusion)#,user=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("aristotle_dse:dataSetSpecification",args=[dss.id]))
    else:
        form = forms.EditDataElementInclusionForm(instance=inclusion)#,user=request.user)

    return render(request,"aristotle_dse/actions/edit_inclusion.html",
            {"item":inclusion,
             "form":form,
                }
            )

def editClusterInclusion(request,dss_id,cluster_id):
    dss = get_object_or_404(aristotle_dse.models.DataSetSpecification,id=dss_id)
    cluster=get_object_or_404(aristotle_dse.models.DataSetSpecification,id=cluster_id)
    if not (user_can_edit(request.user,dss) and user_can_view(request.user,cluster_id)):
        raise PermissionDenied
    inclusion = get_object_or_404(aristotle_dse.models.DSSClusterInclusion,child = cluster,dss = dss)


    if request.method == 'POST': # If the form has been submitted...
        form = forms.EditClusterInclusionForm(request.POST,instance=inclusion)#,user=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("aristotle_dse:dataSetSpecification",args=[dss.id]))
    else:
        form = forms.EditClusterInclusionForm(instance=inclusion)#,user=request.user)

    return render(request,"aristotle_dse/actions/edit_inclusion.html",
            {"item":inclusion,
             "form":form,
                }
            )
    

class DynamicTemplateView(TemplateView):
    def get_template_names(self):
        return ['aristotle_dse/static/%s.html' % self.kwargs['template']]
