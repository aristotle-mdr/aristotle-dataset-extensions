from django.db.models import signals
import aristotle_dse
import aristotle_mdr
from django.conf import settings

def loadTestData(**kwargs):
    print "Loading Aristotle-DSE test data because DEBUG is set to True."
    signals.post_save.disconnect(aristotle_mdr.models.concept_saved)
    aristotle_dse.models.testData()
    signals.post_save.connect(aristotle_mdr.models.concept_saved)

if getattr(settings, 'DEBUG', "") == True:
    signals.post_syncdb.connect(loadTestData, sender=aristotle_dse.models)