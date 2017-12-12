from django.core.cache import cache


def count_api_requests_middleware(get_response):
    """
    Count the number of requests made to the API
    """
    def middleware(request):
        response = get_response(request)
        print(request.method)
        if (request.path.startswith('/api/v1/cpf-blacklist') or
            'cpf' in request.GET and request.method == 'GET'):
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


