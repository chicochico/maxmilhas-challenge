from django.core.exceptions import ValidationError

from django.db import IntegrityError
from rest_framework import serializers

from cpf.models import CPF, CPFBlacklist


class CPFBlacklistSerializer(serializers.Serializer):
    cpf = serializers.SerializerMethodField()
    added_on = serializers.DateTimeField()

    def get_cpf(self, obj):
        return obj.cpf.number


class CPFStatusSerializer(serializers.Serializer):
    cpf = serializers.SerializerMethodField()
    blacklisted = serializers.SerializerMethodField()

    def get_cpf(self, cpf_number):
        if cpf_number is not None:
            cpf = CPF(number=cpf_number)
            if cpf.is_valid():
                return cpf.number
            else:
               raise serializers.ValidationError('invalid CPF')
        else:
            raise serializers.ValidationError('CPF number is required.')

    def get_blacklisted(self, cpf_number):
        return CPFBlacklist.is_blacklisted(cpf_number)


class AddCPFToBlacklistSerializer(serializers.Serializer):
    status = serializers.SerializerMethodField()

    def get_status(self, cpf_number):
        try:
            CPFBlacklist.add_cpf(cpf_number)
            return 'CPF successfully blacklisted.'
        except ValidationError:
            raise serializers.ValidationError('Invalid CPF number.')
        except IntegrityError:
            raise serializers.ValidationError('CPF already in blacklist. Not added.')

