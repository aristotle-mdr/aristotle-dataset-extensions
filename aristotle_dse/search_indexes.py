import models
from haystack import indexes
from aristotle_mdr.search_indexes import conceptIndex

class DataSetSpecificationIndex(conceptIndex, indexes.Indexable):
    def get_model(self):
        return models.DataSetSpecification

class DataSource(conceptIndex, indexes.Indexable):
    def get_model(self):
        return models.DataSource
