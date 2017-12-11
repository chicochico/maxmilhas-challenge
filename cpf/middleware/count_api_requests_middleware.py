from django.core.cache import cache


def count_api_requests_middleware(get_response):
    """
    Count the number of requests made to the API
    """
    def middleware(request):
        response = get_response(request)
        if request.path.startswith('/api'):
            increment_requests_count()
        return response

    return middleware


def increment_requests_count():
    """
    This function increments the total
    requests count since starting the server
    """
    current_count = cache.get('requests_count')
    if current_count is not None:
        cache.set('requests_count', current_count + 1)
    else:
        cache.set('requests_count', 1)


