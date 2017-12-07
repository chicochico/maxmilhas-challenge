from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from cpf.models import CPF, CPFBlacklist

class TestCPFInsertion(TestCase):
    def setUp(self):
        CPF.create('234.787.863-80')
        CPF.create('731.326.163-20')
        CPFBlacklist.add_cpf('731.326.163-20')

    def test_cpf_is_inserted(self):
        self.assertTrue(CPF.objects.filter(number='234.787.863-80').exists())

    def test_cpf_validation(self):
        with self.assertRaises(ValidationError):
            CPF.create('foobar')

    def test_invalid_cpf(self):
        with self.assertRaises(ValidationError):
            CPF.create('234.787.863-81')

    def test_invalid_cpf_with_letters(self):
        with self.assertRaises(ValidationError):
            CPF.create('234.7A7.863-81')

    def test_invalid_cpf_with_repeated_digits(self):
        with self.assertRaises(ValidationError):
            CPF.create('111.111.111-11')

    def test_cpf_number_is_unique(self):
        with self.assertRaises(ValidationError):
            CPF.create(number='234.787.863-80')

    def test_blacklist_cpf(self):
        self.assertTrue(CPFBlacklist.is_blacklisted('731.326.163-20'))

    def test_remove_cpf_from_blacklist(self):
        CPFBlacklist.remove_cpf('731.326.163-20')
        self.assertFalse(CPFBlacklist.is_blacklisted('731.326.163-20'))

    def test_non_existing_cpf_is_not_blacklisted(self):
        number = '625.634.154-62'
        self.assertFalse(CPFBlacklist.is_blacklisted(number))


