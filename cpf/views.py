from datetime import datetime
from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, list_route

from cpf.models import CPFBlacklist
from cpf.serializers import CPFBlacklistSerializer


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


class ListBlacklistedCPF(viewsets.ViewSet):
    """
    list: list all blacklisted CPFs
    """
    def list(self, request):
        increment_requests_count()
        queryset = CPFBlacklist.objects.all()
        serializer = CPFBlacklistSerializer(queryset, many=True)
        return Response(serializer.data)


    @list_route(methods=['get'], url_path='check-cpf', url_name='check-cpf')
    def check_cpf(self, request):
        """
        Check if a CPF is blacklisted
        """
        increment_requests_count()
        cpf_number = request.query_params.get('number', None)
        if CPFBlacklist.is_blacklisted(cpf_number):
            return Response({"cpf": cpf_number, "blacklisted": True})
        else:
            return Response({"cpf": cpf_number, "blacklisted": False})


@api_view(['GET'])
def status(request):
    """
    View server information
    number of requests since startup
    time since startup
    number of blacklisted CPFs
    """
    increment_requests_count()
    return Response({
        'requests_count': cache.get('requests_count'),
        'uptime': str(datetime.now() - settings.START_TIME),
        'blacklisted_cpf_count': CPFBlacklist.objects.all().count()
    })

