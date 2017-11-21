from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import transaction
from django.forms.models import modelformset_factory
from django.forms.widgets import HiddenInput
from django.http import HttpResponseRedirect, Http404
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext as _

from reversion import revisions as reversion

import aristotle_mdr as aristotle
from aristotle_mdr.contrib.generic.views import ConfirmDeleteView
from aristotle_mdr.contrib.generic.forms import HiddenOrderModelFormSet
from aristotle_mdr.perms import (
    user_can_view, user_can_edit, user_in_workgroup,
    user_is_workgroup_manager, user_can_change_status
)
from aristotle_mdr.utils import construct_change_message

import aristotle_dse
from aristotle_dse import forms


@reversion.create_revision()
def addDataElementsToDSS(request, dss_id):
    dss = get_object_or_404(aristotle_dse.models.DataSetSpecification, id=dss_id)
    if not user_can_edit(request.user, dss):
        raise PermissionDenied
    qs = aristotle.models.DataElement.objects.filter().visible(request.user)
    if request.method == 'POST':
        form = forms.AddDataElementsToDSSForm(request.POST, user=request.user, qs=qs, dss=dss)
        if form.is_valid():
            cardinality = form.cleaned_data['cardinality']
            maxOccurs = form.cleaned_data['maximum_occurances']
            for de in form.cleaned_data['dataElements']:
                dss.addDataElement(
                    data_element=de,
                    maximum_occurances=maxOccurs,
                    cardinality=cardinality
                )
            return HttpResponseRedirect(reverse("aristotle_mdr:item", args=[dss.id]))
    else:
        form = forms.AddDataElementsToDSSForm(user=request.user, qs=qs, dss=dss)

    return render(
        request,
        "aristotle_dse/actions/addDataElementsToDSS.html",
        {
            "item": dss,
            "form": form,
        }
    )


@reversion.create_revision()
def addClustersToDSS(request, dss_id):
    dss = get_object_or_404(aristotle_dse.models.DataSetSpecification, id=dss_id)
    if not user_can_edit(request.user, dss):
        raise PermissionDenied
    qs = aristotle_dse.models.DataSetSpecification.objects.filter().visible(request.user)
    if request.method == 'POST':
        form = forms.AddClustersToDSSForm(request.POST, user=request.user, qs=qs, dss=dss)
        if form.is_valid():
            cardinality = form.cleaned_data['cardinality']
            maxOccurs = form.cleaned_data['maximum_occurances']
            for child_dss in form.cleaned_data['clusters']:
                dss.addCluster(
                    child=child_dss,
                    maximum_occurances=maxOccurs,
                    cardinality=cardinality
                )
            return HttpResponseRedirect(reverse("aristotle_mdr:item", args=[dss.id]))
    else:
        form = forms.AddClustersToDSSForm(user=request.user, qs=qs, dss=dss)

    return render(
        request,
        "aristotle_dse/actions/addClustersToDSS.html",
        {
            "item": dss,
            "form": form,
        }
    )


class RemoveDEFromDSS(ConfirmDeleteView):
    item_kwarg="dss_id"
    form_title="Remove data element from dataset"
    form_delete_button_text="Remove data element"

    @reversion.create_revision()
    def perform_deletion(self):
        de_id = self.kwargs['de_id']
        dss_id = self.kwargs['dss_id']
        de = get_object_or_404(aristotle.models.DataElement, id=de_id)
        dss = get_object_or_404(aristotle_dse.models.DataSetSpecification, id=dss_id)
        if user_can_view(self.request.user, de) and user_can_edit(self.request.user, dss):
            dss.dssdeinclusion_set.filter(data_element=de).delete()
            messages.success(
                self.request,
                _('The Data Element "%(de_name)s" was removed from the dataset "%(dss_name)s".') % {
                    "de_name": de.name, "dss_name": dss.name
                }
            )
        else:
            raise PermissionDenied

    def warning_text(self):
        de = get_object_or_404(aristotle.models.DataElement, id=self.kwargs['de_id'])
        dss = get_object_or_404(aristotle_dse.models.DataSetSpecification, id=self.kwargs['dss_id'])
        return _(
            'You are about to detatch the data element "%(de_name)s" from the dataset "%(dss_name)s". \n'
            'This data element will still exist in the registry, but will no longer be linked to this Data Set Specification. \n\n'
            'Click "Remove data element" below to confirm, or click "Cancel" to return'
        ) % {
            "de_name": de.name, "dss_name": dss.name
        }


class RemoveClusterFromDSS(ConfirmDeleteView):
    item_kwarg="dss_id"
    form_title="Remove data element from this dataset"

    @reversion.create_revision()
    def perform_deletion(self):
        cluster_id = self.kwargs['cluster_id']
        dss_id = self.kwargs['dss_id']
        cluster = get_object_or_404(aristotle_dse.models.DataSetSpecification, id=cluster_id)
        dss = get_object_or_404(aristotle_dse.models.DataSetSpecification, id=dss_id)
        if user_can_view(self.request.user, cluster) and user_can_edit(self.request.user, dss):
            dss.dssclusterinclusion_set.filter(child=cluster).delete()
            messages.success(
                self.request,
                _('The cluster "%(cl_name)s" was removed from the dataset "%(dss_name)s".') % {
                    "cl_name": cluster.name, "dss_name": dss.name
                }
            )
        else:
            raise PermissionDenied


@reversion.create_revision()
def editDataElementInclusion(request, dss_id, de_id):
    dss = get_object_or_404(aristotle_dse.models.DataSetSpecification, id=dss_id)
    de = get_object_or_404(aristotle.models.DataElement, id=de_id)
    if not (user_can_edit(request.user, dss) and user_can_view(request.user, de)):
        raise PermissionDenied
    inclusion = get_object_or_404(aristotle_dse.models.DSSDEInclusion, data_element=de, dss=dss)

    if request.method == 'POST':
        form = forms.EditDataElementInclusionForm(request.POST, instance=inclusion)  # , user=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("aristotle_mdr:item", args=[dss.id]))
    else:
        form = forms.EditDataElementInclusionForm(instance=inclusion)  # , user=request.user)

    return render(
        request,
        "aristotle_dse/actions/edit_inclusion.html",
        {
            "item": inclusion,
            "form": form,
        }
    )


@reversion.create_revision()
def editClusterInclusion(request, dss_id, cluster_id):
    dss = get_object_or_404(aristotle_dse.models.DataSetSpecification, id=dss_id)
    cluster = get_object_or_404(aristotle_dse.models.DataSetSpecification, id=cluster_id)
    if not (user_can_edit(request.user, dss) and user_can_view(request.user, cluster_id)):
        raise PermissionDenied
    inclusion = get_object_or_404(aristotle_dse.models.DSSClusterInclusion, child=cluster, dss=dss)

    if request.method == 'POST':
        form = forms.EditClusterInclusionForm(request.POST, instance=inclusion)  # , user=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("aristotle_mdr:item", args=[dss.id]))
    else:
        form = forms.EditClusterInclusionForm(instance=inclusion)  # , user=request.user)

    return render(
        request,
        "aristotle_dse/actions/edit_inclusion.html",
        {
            "item": inclusion,
            "form": form,
        }
    )


@reversion.create_revision()
def editInclusionDetails(request, dss_id, inc_type, cluster_id):
    dss = get_object_or_404(aristotle_dse.models.DataSetSpecification, id=dss_id)

    if inc_type not in ['cluster', 'data_element']:
        raise Http404
    item = get_object_or_404(aristotle_dse.models.DataSetSpecification, pk=dss_id)
    if not user_can_edit(request.user, item):
        if request.user.is_anonymous():
            return redirect(reverse('friendly_login') + '?next=%s' % request.path)
        else:
            raise PermissionDenied

    item_type, field_name = {
        'cluster': (aristotle_dse.models.DataSetSpecification, 'child'),
        'data_element': (aristotle.models.DataElement, 'data_element'),
        }.get(inc_type)

    cluster=get_object_or_404(item_type, id=cluster_id)
    if not (user_can_edit(request.user, dss) and user_can_view(request.user, cluster_id)):
        raise PermissionDenied
    inclusion = get_object_or_404(aristotle_dse.models.DSSClusterInclusion, child=cluster, dss=dss)

    if request.method == 'POST':
        form = forms.EditClusterInclusionForm(request.POST, instance=inclusion)  # , user=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("aristotle_mdr:item", args=[dss.id]))
    else:
        form = forms.EditClusterInclusionForm(instance=inclusion)  # , user=request.user)

    return render(
        request,
        "aristotle_dse/actions/edit_inclusion.html",
        {
            "item": inclusion,
            "form": form,
            "include_type": inc_type,
        }
    )


def editInclusionOrder(request, dss_id, inc_type):
    if inc_type not in ['cluster', 'data_element']:
        raise Http404
    item = get_object_or_404(aristotle_dse.models.DataSetSpecification, pk=dss_id)
    if not user_can_edit(request.user, item):
        if request.user.is_anonymous():
            return redirect(reverse('friendly_login') + '?next=%s' % request.path)
        else:
            raise PermissionDenied

    item_type, field_name = {
        'cluster': (aristotle_dse.models.DSSClusterInclusion, 'child'),
        'data_element': (aristotle_dse.models.DSSDEInclusion, 'data_element'),
        }.get(inc_type)

    num_values = item_type.objects.filter(dss=item.id).count()
    if num_values > 0:
        extra = 0
    else:
        extra = 1

    ValuesFormSet = modelformset_factory(
        item_type,
        formset=HiddenOrderModelFormSet,
        can_order=True,
        fields=('id',),
        extra=extra
    )

    if request.method == 'POST':
        formset = ValuesFormSet(request.POST, request.FILES)
        if formset.is_valid():
            with transaction.atomic(), reversion.create_revision():
                item.save()  # do this to ensure we are saving reversion records for the DSS, not just the values
                formset.save(commit=False)
                for form in formset.forms:
                    if form['id'].value() not in [deleted_record['id'].value() for deleted_record in formset.deleted_forms]:
                        inc = item_type.objects.get(pk=form['id'].value())
                        if inc.dss != item:
                            raise PermissionDenied
                        inc.order = form['ORDER'].value()
                        # inc.maximum_occurances = form['maximum_occurances'].value()
                        # value = form.save(commit=False) #Don't immediately save, we need to attach the value domain
                        # value.dss = item
                        inc.save()
                for obj in formset.deleted_objects:
                    obj.delete()
                reversion.set_user(request.user)
                reversion.set_comment(construct_change_message(request, None, [formset, ]))

                return redirect(reverse("aristotle_mdr:item", args=[item.id]))
    else:
        formset = ValuesFormSet(
            queryset=item_type.objects.filter(dss=item.id),
        )
    return render(
        request,
        "aristotle_dse/actions/edit_inclusion_order.html",
        {'item': item, 'formset': formset, 'include_type': inc_type, 'value_model': item_type, }
    )


class DynamicTemplateView(TemplateView):
    def get_template_names(self):
        return ['aristotle_dse/static/%s.html' % self.kwargs['template']]
