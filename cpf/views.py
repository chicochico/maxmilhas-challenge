from datetime import datetime
from django.conf import settings
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route, api_view
from cpf.models import CPF, CPFBlacklist
from cpf.serializers import CPFBlacklistSerializer
from cpf.serializers import CPFStatusSerializer
from cpf.serializers import AddCPFToBlacklistSerializer


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


class CPFBlacklistViewSet(viewsets.ViewSet):
    """
    CPF blacklist endpoints
    """
    queryset = CPFBlacklist.objects.all()
    serializer_class = CPFBlacklistSerializer
    lookup_field = 'cpf_number'

    def list(self, request):
        """
        Show all blacklisted CPF
        """
        increment_requests_count()
        serializer = CPFBlacklistSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'], url_path='status/(?P<cpf_number>.+)')
    def check_cpf_status(self, request, cpf_number=None):
        """
        Check if a CPF is blacklisted
        """
        increment_requests_count()
        serializer = CPFStatusSerializer(cpf_number, many=False)
        return Response(serializer.data)

    @list_route(methods=['post'], url_path='add/(?P<cpf_number>.+)')
    def add_to_blacklist(self, request, cpf_number=None):
        """
        Add a new CPF to the blacklist
        """
        increment_requests_count()
        serializer = AddCPFToBlacklistSerializer(cpf_number)
        return Response(serializer.data)


@api_view(['GET'])
def server_status(request):
    """
    View server information
    number of requests since startup
    time since startup
    number of blacklisted CPFs
    """
    return Response({
        'requests_count': cache.get('requests_count'),
        'uptime': str(datetime.now() - settings.START_TIME),
        'blacklisted_cpf_count': CPFBlacklist.objects.all().count()
    })

