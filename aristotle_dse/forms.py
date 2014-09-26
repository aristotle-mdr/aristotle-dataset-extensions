import autocomplete_light
autocomplete_light.autodiscover()

from django import forms
from aristotle_mdr.perms import user_can_view, user_can_edit
from aristotle_dse.models import CARDINALITY

class AddDataElementsToDSSForm(forms.Form):
    cardinality = forms.ChoiceField(choices=CARDINALITY,widget=forms.RadioSelect)
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
