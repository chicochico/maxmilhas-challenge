from django.test import TestCase
from django.core.exceptions import ValidationError
from cpf.models import CPF, CPFBlacklist

class TestCPFInsertion(TestCase):
    def setUp(self):
        CPF.create('23478786380')
        CPF.create('73132616320')
        CPFBlacklist.add_cpf('73132616320')

    def test_cpf_is_inserted(self):
        self.assertTrue(CPF.objects.filter(number='23478786380').exists())

    def test_cpf_validation(self):
        with self.assertRaises(ValidationError):
            CPF.create('foobar')

    def test_invalid_cpf(self):
        with self.assertRaises(ValidationError):
            CPF.create('23478786381')

    def test_invalid_cpf_with_letters(self):
        with self.assertRaises(ValidationError):
            CPF.create('2347A786381')

    def test_invalid_cpf_with_repeated_digits(self):
        with self.assertRaises(ValidationError):
            CPF.create('11111111111')

    def test_cpf_number_is_unique(self):
        with self.assertRaises(ValidationError):
            CPF.create(number='23478786380')

    def test_blacklist_cpf(self):
        self.assertTrue(CPFBlacklist.is_blacklisted('73132616320'))

    def test_remove_cpf_from_blacklist(self):
        CPFBlacklist.remove_cpf('73132616320')
        self.assertFalse(CPFBlacklist.is_blacklisted('73132616320'))

    def test_non_existing_cpf_is_not_blacklisted(self):
        number = '62563415462'
        self.assertFalse(CPFBlacklist.is_blacklisted(number))
