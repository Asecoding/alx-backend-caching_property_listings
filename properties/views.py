from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property  # Assuming your model is named Propert
from .utils import get_all_properties
@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    properties = Property.objects.all().values()  # You can customize fields
    return JsonResponse(list(properties), safe=False)

def property_list(request):
    properties = get_all_properties()
    return JsonResponse(properties, safe=False)

