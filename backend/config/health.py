from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import redis


def healthz(request):
    """Basic health check"""
    return JsonResponse({'status': 'healthy'}, status=200)


def livez(request):
    """Liveness probe - is the app running?"""
    return JsonResponse({'status': 'alive'}, status=200)


def readyz(request):
    """Readiness probe - can the app serve traffic?"""
    checks = {
        'database': False,
        'cache': False,
    }
    
    # Check database
    try:
        connection.ensure_connection()
        checks['database'] = True
    except Exception as e:
        checks['database_error'] = str(e)
    
    # Check Redis cache
    try:
        cache.set('health_check', 'ok', 10)
        checks['cache'] = cache.get('health_check') == 'ok'
    except Exception as e:
        checks['cache_error'] = str(e)
    
    all_healthy = all([checks['database'], checks['cache']])
    status_code = 200 if all_healthy else 503
    
    return JsonResponse({
        'status': 'ready' if all_healthy else 'not_ready',
        'checks': checks
    }, status=status_code)
