from django.core.cache import cache
from django.http import HttpResponseForbidden

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        path = request.path
        key = f'ratelimit:{ip}:{path}'
        limit = 100  # Adjust as needed
        timeout = 60  # Adjust as needed (seconds)

        count = cache.get(key)
        if count is None:
            cache.set(key, 1, timeout)
        else:
            count += 1
            if count > limit:
                return HttpResponseForbidden("Rate limit exceeded")
            cache.set(key, count, timeout)

        response = self.get_response(request)
        return response
