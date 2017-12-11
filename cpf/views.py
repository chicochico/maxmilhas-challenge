from datetime import datetime
from django.conf import settings
from django.core.cache import cache
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import list_route, api_view
from cpf.models import CPF, CPFBlacklist
from cpf.serializers import CPFBlacklistSerializer
from cpf.serializers import CPFStatusSerializer
from cpf.serializers import CPFSerializer


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


class CPFBlacklistViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """
    CPF Blacklist endpoints

    list: List all CPF in the blacklist
    create: Add a new cpf to the blacklist
    destroy: Remove a cpf from de blacklist
    retrieve: Get the details of a CPF blacklist entry
    """
    queryset = CPFBlacklist.objects.all()
    serializer_class = CPFBlacklistSerializer
    lookup_field = 'cpf__number'


    @list_route(methods=['get'], url_path='check-cpf')
    def check_cpf_status(self, request):
        """
        Check if a CPF is blacklisted, parameters:

        number -- a CPF number in the format XXXXXXXXXXX
        """
        increment_requests_count()
        cpf_number = self.request.query_params.get('number', None)
        serializer = CPFStatusSerializer(cpf_number, many=False)
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

