from rest_framework import serializers
from cpf.models import CPF, CPFBlacklist


class CPFBlacklistSerializer(serializers.Serializer):
    cpf = serializers.SerializerMethodField()
    added_on = serializers.DateTimeField()

    def get_cpf(self, obj):
        return obj.cpf.number

