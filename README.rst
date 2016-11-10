Aristotle Dataset Extensions
============================

The Aristotle Dataset Extensions (Aristotle-DSE) is a `DCAT-compatible <https://www.w3.org/TR/vocab-dcat>`_ extension
to the Aristotle Metadata Registry to provide metadata-aware data registry services.

Aristotle-DSE implements the `W3C DCAT standard <https://www.w3.org/TR/vocab-dcat>`_ for describing dataset resources on the web
and provides 2 additional objects with references described below

:DataSetSpecification: *(Subclass of ISO 11179 concept)*

 A standardised collection of 11179 Data Elements commonly used together to describe a resuable dataset.
 A ``DataSetSpecification`` may be referenced by a ``dcat:Distribution`` to describe the data within the file or
 resource described by the Distribution.
:DistributionDataElement: By assocation``dcat:Distribution`` does not implement a standardised DataSetSpecification,
 it may optionally refer to 0 or more ``DistributionDataElement`` objects which describe

Where a ``dcat:Distribution`` has an association to ``DataSetSpecification`` and number of ``DistributionDataElement`` objects, the details of the ``DistributionDataElement`` should be used for validation and quality purposes.


For reference the full DCAT data model is presented below:

|dcat|

.. |dcat| image:: https://www.w3.org/TR/vocab-dcat/dcat-model.jpg
    :alt: build status
    :scale: 100%
    :target: https://www.w3.org/TR/vocab-dcat
