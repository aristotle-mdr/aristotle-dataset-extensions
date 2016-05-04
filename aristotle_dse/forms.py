import autocomplete_light
autocomplete_light.autodiscover()

from django import forms
from aristotle_mdr.perms import user_can_view, user_can_edit
from aristotle_dse import models

class AddDataElementsToDSSForm(forms.Form):
    cardinality = forms.ChoiceField(choices=models.CARDINALITY,widget=forms.RadioSelect)
    maximum_occurances = forms.IntegerField(min_value=1,initial=1)
                #widget=forms.CheckboxSelectMultiple)
    def __init__(self, *args, **kwargs):
        self.qs = kwargs.pop('qs')
        self.dss = kwargs.pop('dss')
        self.user = kwargs.pop('user')
        super(AddDataElementsToDSSForm, self).__init__(*args, **kwargs)
        self.fields['dataElements']=forms.ModelMultipleChoiceField(
                queryset=self.qs,
                label="Add Data Elements",
                widget=autocomplete_light.MultipleChoiceWidget("AutocompleteDataElement")
                )

    def clean_dataElements(self):
        dataElements = self.cleaned_data['dataElements']
        cleaned = [de for de in dataElements if user_can_view(self.user,de)]
        return cleaned

class EditDataElementInclusionForm(forms.ModelForm):
    class Meta:
        model = models.DSSDEInclusion
        fields = ['maximum_occurances', 'cardinality', 'specific_information', 'conditional_obligation']

class EditClusterInclusionForm(forms.ModelForm):
    class Meta:
        model = models.DSSClusterInclusion
        fields = ['maximum_occurances', 'cardinality', 'specific_information', 'conditional_obligation']


class AddClustersToDSSForm(forms.Form):
    cardinality = forms.ChoiceField(choices=models.CARDINALITY,widget=forms.RadioSelect)
    maximum_occurances = forms.IntegerField(min_value=1,initial=1)

    def __init__(self, *args, **kwargs):
        self.qs = kwargs.pop('qs')
        self.dss = kwargs.pop('dss')
        self.user = kwargs.pop('user')
        super(AddClustersToDSSForm, self).__init__(*args, **kwargs)
        self.fields['clusters']=forms.ModelMultipleChoiceField(
                queryset=self.qs,
                label="Add Clusters",
                widget=autocomplete_light.MultipleChoiceWidget("AutocompleteDataSetSpecification")
                )

    def clean_dataElements(self):
        clusters = self.cleaned_data['clusters']
        cleaned = [dss for dss in clusters if user_can_view(self.user,dss)]
        return cleaned
