from datetime import datetime
from django.conf import settings
from django.core.cache import cache
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import list_route, api_view
from cpf.models import CPF, CPFBlacklist
from api.serializers import CPFBlacklistSerializer
from api.serializers import CPFStatusSerializer
from api.serializers import CPFSerializer


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

    @list_route(methods=['get'], url_path='check-cpf', url_name='check-cpf')
    def check_cpf_status(self, request, number=None):
        """
        Check if a CPF is blacklisted, parameters:

        cpf -- a CPF number in the format XXXXXXXXXXX
        """
        cpf_number = self.request.query_params.get('cpf', None)
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

