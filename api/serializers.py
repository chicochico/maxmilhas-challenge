from django.core.exceptions import ValidationError

from rest_framework import serializers

from cpf.models import CPF, CPFBlacklist


class CPFSerializer(serializers.ModelSerializer):
    """
    Serialize a single CPF instance
    """
    class Meta:
        model = CPF
        fields = ('number',)


class CPFBlacklistSerializer(serializers.ModelSerializer):
    """
    Serialize a CPF Blacklist item with CPF
    number and the date in which it was added
    """
    cpf = CPFSerializer(many=False)

    class Meta:
        model = CPFBlacklist
        fields = ('cpf', 'added_on')
        read_only_fields = ('added_on',)

    def create(self, validated_data):
        cpf_number = validated_data['cpf']['number']
        try:
            return CPFBlacklist.add_cpf(cpf_number)
        except ValidationError:
            raise serializers.ValidationError(
                {'cpf': {'number': ['Invalid CPF number.']}}
            )


class CPFStatusSerializer(serializers.Serializer):
    """
    Status of a CPF, if it is blacklisted or not
    """
    cpf = serializers.SerializerMethodField()
    blacklisted = serializers.SerializerMethodField()

    def get_cpf(self, cpf_number):
        """
        Get the number of the CPF
        raises: ValidationError
        """
        if cpf_number is not None:
            cpf = CPF(number=cpf_number)
            if cpf.is_valid():
                return cpf.number
            else:
                raise serializers.ValidationError(
                    {'number': 'Invalid CPF number.'}
                )
        else:
            raise serializers.ValidationError(
                {'number': 'CPF number is required.'}
            )

    def get_blacklisted(self, cpf_number):
        """
        Get if a CPF is blacklisted
        """
        return CPFBlacklist.is_blacklisted(cpf_number)

