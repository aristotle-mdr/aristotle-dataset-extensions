from django import template
import re

from aristotle_dse.models import CARDINALITY


register = template.Library()


@register.filter
def column_name(dataelement):
    name = re.sub('[^a-zA-Z]+', '', dataelement.name)
    suffix = '_de_'+ str(dataelement.id)
    return name[:30 - (len(suffix))] + suffix


@register.filter
def table_name(dss):
    name = re.sub('[^a-zA-Z]+', '', dss.name)
    suffix = '_dss_' + str(dss.id)
    return name[:30 - (len(suffix))] + suffix


@register.filter
def column_data_type(dataelementinclusion):
    fallback_column = "VARCHAR(4096)"
    if not dataelementinclusion.dataElement.valueDomain:
        column_definition = fallback_column
        if dataelementinclusion.cardinality is not CARDINALITY.mandatory:
            # if its optional, it must be nullable.
            column_definition += " NULL "
        return column_definition

    valuedomain = dataelementinclusion.dataElement.valueDomain
    data_type = valuedomain.data_type.name
    _format = valuedomain.format
    if data_type == "Boolean":
        column_definition = "BOOLEAN"
    elif data_type == "String":
        if valuedomain.maximum_length:
            column_definition = "VARCHAR(%s)" % valuedomain.maximum_length
        else:
            column_definition = fallback_column
    elif data_type == "Date/Time":
        column_definition = "TIMESTAMP"

    elif data_type in ["Number", "Currency"]:
        if _format and len(_format.split('.')) == 2:
            f = _format.split('.')
            size = len(f[0]) + len(f[1])
            decimals = len(f[1])
            column_definition = "DECIMAL(%s,%s)" % (size, decimals)
        elif valuedomain.maximum_length:
            column_definition = "FLOAT(%s)" % valuedomain.maximum_length
        else:
            column_definition = "FLOAT(16)"
    else:  # Catch all.
        column_definition = fallback_column

    if dataelementinclusion.cardinality is not CARDINALITY.mandatory:
        # if its optional, it must be nullable.
        column_definition += " NULL "

    if _format:
        column_definition += "/* Format should follow: %s */" % _format

    return column_definition
