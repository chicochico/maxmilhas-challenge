from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from cpf.models import CPF, CPFBlacklist


class CPFBlacklistTestCase(APITestCase):
    def setUp(self):
        """
        Setup data in the database to test API endpoints
        """
        CPFBlacklist.add_cpf('19712271374')
        CPFBlacklist.add_cpf('82248784066')

    def test_show_full_blacklist(self):
        """
        Get the list of all channels
        """
        url = reverse('blacklist-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['cpf']['number'], '19712271374')
        self.assertEqual(response.data[1]['cpf']['number'], '82248784066')

    def test_get_single_cpf(self):
        """
        Get a single entry by the CPF number
        """
        url = reverse('blacklist-detail', args=['19712271374'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cpf']['number'], '19712271374')

    def test_non_existing_cpf_is_not_blacklisted(self):
        """
        A non existing CPF retunrns 404
        """
        url = reverse('blacklist-detail', args=['this_does_not_exist'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "Not found.")

    def test_add_cpf_to_blacklist(self):
        """
        Add a CPF to the blacklist
        """
        url = reverse('blacklist-list')
        data = {'cpf': {'number': '86584413853'}}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['cpf']['number'], '86584413853')

    def test_add_invalid_cpf_to_blacklist(self):
        """
        A invalid CPF number should return error
        """
        url = reverse('blacklist-list')
        data = {'cpf': {'number': '11111111111'}}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['cpf']['number'], ['Invalid CPF number.'])

    def test_add_invalid_cpf_too_long(self):
        """
        A invalid CPF that is too long
        """
        url = reverse('blacklist-list')
        data = {'cpf': {'number': '111111111111111111'}}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['cpf']['number'], ['Ensure this field has no more than 11 characters.'])

    def test_add_invalid_cpf_emtpy(self):
        """
        CPF number field cannot be emtpy
        """
        url = reverse('blacklist-list')
        data = {'cpf': {'number': ''}}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['cpf']['number'], ['This field may not be blank.'])

    def test_add_duplicated_cpf_to_blacklist(self):
        """
        A CPF in the blacklist should be unique
        """
        url = reverse('blacklist-list')
        data = {'cpf': {'number': '19712271374'}}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['cpf']['number'], ['CPF with this number already exists.'])

    def test_remove_cpf_from_blacklist(self):
        """
        Remove a CPF from the blacklist by its number
        """
        # remove
        url = reverse('blacklist-detail', args=['19712271374'])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # try to get it
        response2 = self.client.get(url)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_parameter_check_blacklisted_cpf(self):
        """
        Use query parameters to get the status of a CPF by the number
        """
        url = reverse('blacklist-check-cpf') + '?cpf=19712271374'
        response = self.client.get(url)
        expected = {
            'cpf': '19712271374',
            'blacklisted': True,
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

    def test_query_parameter_check_whitelisted_cpf(self):
        """
        Test a CPF that is not in the blacklist
        """
        url = reverse('blacklist-check-cpf') + '?cpf=57794218209'
        response = self.client.get(url)
        expected = {
            'cpf': '57794218209',
            'blacklisted': False,
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

    def test_query_parameter_invalid_cpf(self):
        """
        Test CPF validation from query parameter
        """
        url = reverse('blacklist-check-cpf') + '?cpf=invalid-cpf-number'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'number': 'Invalid CPF number.'})

    def test_get_server_status(self):
        """
        Test the server status endpoint
        """
        url = reverse('server-status')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('requests_count' in response.data)
        self.assertTrue('uptime' in response.data)
        self.assertTrue('blacklisted_cpf_count' in response.data)


