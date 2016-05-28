from django.test import TestCase

import aristotle_mdr.models as MDR
from django.core.urlresolvers import reverse
from aristotle_mdr.tests.utils import ManagedObjectVisibility
from aristotle_mdr.tests.main.test_html_pages import LoggedInViewConceptPages
from aristotle_mdr.tests.main.test_admin_pages import AdminPageForConcept

from django.test.utils import setup_test_environment
setup_test_environment()

from aristotle_dse import models

def setUpModule():
    from django.core.management import call_command
    call_command('loadhelp', 'aristotle_help/concept_help/*', verbosity=0, interactive=False)

class LoggedInViewDSSConceptPages(LoggedInViewConceptPages):
    def get_help_page(self):
        return reverse('aristotle_dse:about',args=[self.item1._meta.model_name])

class DataSetSpecificationVisibility(ManagedObjectVisibility,TestCase):
    def setUp(self):
        super(DataSetSpecificationVisibility, self).setUp()
        self.item = models.DataSetSpecification.objects.create(name="Test DSS",
            workgroup=self.wg,
            )

class DataSetSpecificationAdmin(AdminPageForConcept,TestCase):
    itemType=models.DataSetSpecification
    form_defaults={
        'dssdeinclusion_set-TOTAL_FORMS':0,
        'dssdeinclusion_set-INITIAL_FORMS':0,
        'dsscdeinclusion_set-MAX_NUM_FORMS':1,
        'dssclusterinclusion_set-TOTAL_FORMS':0,
        'dssclusterinclusion_set-INITIAL_FORMS':0,
        'dssclusterinclusion_set-MAX_NUM_FORMS':1,
        }

class DataSetSpecificationViewPage(LoggedInViewDSSConceptPages,TestCase):
    url_name='datasetspecification'
    itemType=models.DataSetSpecification
    def get_help_page(self):
        return reverse('aristotle_dse:about',args=[self.item1._meta.model_name])
    def test_help_page_exists(self):
        self.logout()
        response = self.client.get(self.get_help_page())
        self.assertEqual(response.status_code,200)
    def test_add_data_element(self):
        de,created = MDR.DataElement.objects.get_or_create(name="Person-sex, Code N",
            workgroup=self.wg1,definition="The sex of the person with a code.",
            )
        self.item1.addDataElement(de)
        self.assertTrue(self.item1.data_elements.count(),1)

    def test_cascade_action(self):
        self.logout()
        check_url = reverse('aristotle:check_cascaded_states', args=[self.item1.pk])
        response = self.client.get(self.get_page(self.item1))
        self.assertEqual(response.status_code,302)
        self.assertTrue(check_url not in response.content)
        
        response = self.client.get(check_url)
        self.assertTrue(response.status_code,403)

        self.login_editor()
        response = self.client.get(self.get_page(self.item1))
        self.assertEqual(response.status_code,200)
        self.assertTrue(check_url in response.content)

