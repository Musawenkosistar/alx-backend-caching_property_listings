from django.shortcuts import render
from .utils import get_all_properties


def property_list(request):
    properties = get_all_properties()
    return render(request, 'properties/property_list.html', {
        'properties': properties
    })

