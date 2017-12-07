from django.test import TestCase
from cpf.models import CPF, CPF_Blacklist


class TestCPFInsertion(TestCase):
    def setUp(self):
        self.cpf = CPF.create('234.787.863-80')

    def test_cpf_is_inserted(self):
        self.assertTrue(CPF.objects.get(number='234.787.863-80').exists())

    def test_cpf_validation(self):
        with self.assertRaises(ValidationError):
            CPF.create('foobar')

    def test_cpf_validation_digits(self):
        with self.assertRaises(ValidationError):
            CPF.create('234.787.863-81')

    def test_invalid_cpf_with_repeated_digits(self):
        with self.assertRaises(ValidationError):
            CPF.create('111.111.111-11')

    def test_cpf_number_is_unique(self):
        with self.assertRaises(IntegrityError):
            Channel.objects.create(name='234.787.863-80')

    def test_blacklist_cpf(self):
        CPF_Blacklist.add_cpf(self.cpf)
        self.assertTrue(CPF_Blacklist.is_blacklisted(self.cpf))

    def test_remove_cpf_from_blacklist(self):
        CPF_Blacklist.remove_cpf(self.cpf)
        self.assertFalse(CPF_Blacklist.is_blacklisted(self.cpf))

    def test_non_existing_cpf_is_not_blacklisted(self):
        number = '625.634.154-62'
        self.assertFalse(CPF_Blacklist.is_blacklisted(number))


