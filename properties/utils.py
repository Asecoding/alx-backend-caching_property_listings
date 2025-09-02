from django.core.cache import cache
from .models import Property

def get_all_properties():
    cached_properties = cache.get('all_properties')
    if cached_properties is not None:
        return cached_properties

    queryset = list(Property.objects.all().values())  # Convert to list for serialization
    cache.set('all_properties', queryset, timeout=3600)  # Cache for 1 hour
    return queryset

