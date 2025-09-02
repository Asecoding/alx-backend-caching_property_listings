from django.core.cache import cache
from .models import Property
import logging
from django_redis import get_redis_connection

def get_all_properties():
    cached_properties = cache.get('all_properties')
    if cached_properties is not None:
        return cached_properties

    queryset = list(Property.objects.all().values())  # Convert to list for serialization
    cache.set('all_properties', queryset, timeout=3600)  # Cache for 1 hour
    return queryset

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    try:
        redis_conn = get_redis_connection("default")
        info = redis_conn.info()

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total = hits + misses

        hit_ratio = (hits / total) if total > 0 else None

        metrics = {
            "keyspace_hits": hits,
            "keyspace_misses": misses,
            "hit_ratio": round(hit_ratio, 4) if hit_ratio is not None else "N/A"
        }

        logger.info(f"Redis Cache Metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Error retrieving Redis metrics: {e}")
        return {
            "keyspace_hits": "Error",
            "keyspace_misses": "Error",
            "hit_ratio": "Error"
        }

