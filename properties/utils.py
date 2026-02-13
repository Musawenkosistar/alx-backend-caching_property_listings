from django.core.cache import cache
from .models import Property


def get_all_properties():
    """
    Returns all Property objects.
    Uses Redis cache (low-level API) for 1 hour.
    """

    properties = cache.get('all_properties')

    if properties is None:
        properties = Property.objects.all()
        cache.set('all_properties', properties, 3600)  # Cache for 1 hour

    return properties
