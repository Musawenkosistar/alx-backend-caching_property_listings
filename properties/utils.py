from django.core.cache import cache
from .models import Property
import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)


def get_redis_cache_metrics():
    """
    Retrieves Redis cache hit/miss metrics and calculates hit ratio.
    """

    redis_conn = get_redis_connection("default")
    info = redis_conn.info()

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)

    total_requests = hits + misses

    if total_requests > 0:
        hit_ratio = hits / total_requests
    else:
        hit_ratio = 0

    metrics = {
        "keyspace_hits": hits,
        "keyspace_misses": misses,
        "hit_ratio": hit_ratio,
    }

    logger.info(f"Redis Cache Metrics: {metrics}")

    return metrics

def get_all_properties():
    """
    Returns all Property objects.
    Uses Redis cache (low-level API) for 1 hour.
    """

    properties = cache.get('all_properties')

    if properties is None:
        properties = Property.objects.all()
        cache.set('all_properties', properties, 3600)

    return properties
