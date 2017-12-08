from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from cpf.models import CPFBlacklist
from cpf.serializers import CPFBlacklistSerializer


class ListBlacklistedCPF(viewsets.ViewSet):
    def list(self, request):
        queryset = CPFBlacklist.objects.all()
        serializer = CPFBlacklistSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def check_cpf(request):
    cpf_number = request.query_params.get('number', None)
    if CPFBlacklist.is_blacklisted(cpf_number):
        return Response({"cpf": cpf_number, "blacklisted": True})
    else:
        return Response({"cpf": cpf_number, "blacklisted": False})
