from django.db import models
from django.core.exceptions import ValidationError

class CPF(models.Model):
    """
    CPF - Cadastro de pessoa fisica
    """
    number = models.CharField(
        max_length=14,
        null=False,
        blank=False,
        unique=True,
    )

    class Meta:
        verbose_name = 'CPF'
        verbose_name_plural = 'CPFs'

    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(CPF, self).save(*args, **kwargs)

    @classmethod
    def create(cls, number):
        """
        Create a new CPF and save it to the database
        """
        return cls.objects.create(number=number)

    def clean(self):
        """
        CPF validation logic
        """
        def checksum(numbers):
            """
            Calculates checksum
            """
            lenght = len(numbers) + 1
            result = sum([i * j for i, j in zip(numbers, range(lenght, 1, -1))]) % 11
            if result < 2:
                return 0
            else:
                return 11 - result

        if len(self.number) != 14:
            raise ValidationError('invalid CPF')

        digits = list(''.join(self.number[:11].split('.')))
        validation_digits = list(self.number[12:14])

        try:
            numbers = [int(n) for n in digits]
            checksum_numbers = [int(n) for n in validation_digits]
        except ValueError:
            raise ValidationError('invalid CPF')

        sum1 = checksum(numbers)
        numbers.append(sum1)
        sum2 = checksum(numbers)

        if (sum1 != checksum_numbers[0] or
            sum2 != checksum_numbers[1] or
            len(set(numbers + checksum_numbers)) == 1):
            # checksum don't match or all the same digits
            raise ValidationError('invalid CPF')



class CPFBlacklist(models.Model):
    """
    Blaclist for CPFs
    """
    cpf = models.OneToOneField(
        CPF,
        on_delete=models.CASCADE,
    )

    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Blacklisted CPF'
        verbose_name_plural = 'Blacklisted CPFs'

    def __str__(self):
        return self.cpf.number

    @classmethod
    def add_cpf(cls, cpf_number):
        """
        Add a new CPF to the blacklist
        cpf: CPF object to be added
        returns: Added CPF blacklist object
        """
        cpf, _ = CPF.objects.get_or_create(number=cpf_number)
        return cls.objects.create(cpf=cpf)

    @classmethod
    def remove_cpf(cls, cpf_number):
        """
        Remove a CPF from the blacklist
        cpf: the cpf to be removed
        returns: None
        raises: DoesNotExist
        """
        try:
            cls.objects.get(cpf__number=cpf_number).delete()
        except CPFBlacklist.DoesNotExist:
            raise

    @classmethod
    def is_blacklisted(cls, cpf_number):
        return cls.objects.filter(cpf__number=cpf_number).exists()
