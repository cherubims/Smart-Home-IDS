from django.test import TestCase
from .models import NetworkTraffic
from rest_framework.test import APIClient
from rest_framework import status

''' TEST MODELS
1. Test the integrity NetworkTraffic model to ensure correct representation of dataset fields.
2. Validate data as expected.
'''
class NetworkTrafficModelTest(TestCase):

    def setUp(self):
        # Create a sample record with all required fields populated
        self.traffic_record = NetworkTraffic.objects.create(
            duration=10,
            protocol_type='TCP',
            service='http',
            flag='SF',
            src_bytes=1500,
            dst_bytes=3500,
            land=False,  # BooleanField
            wrong_fragment=0,
            urgent=0,
            hot=0,
            logged_in=True,  # BooleanField
            num_compromised=0,
            count=2,
            srv_count=3,
            serror_rate=0.0,
            rerror_rate=0.0,
            same_srv_rate=1.0,
            diff_srv_rate=0.0,
            srv_diff_host_rate=0.0,
            dst_host_count=255,
            dst_host_srv_count=255,
            dst_host_same_srv_rate=1.0,
            dst_host_diff_srv_rate=0.0,
            attack=False  # BooleanField
        )

    def test_str_representation(self):
        # Test string representation of the NetworkTraffic model
        self.assertEqual(
            str(self.traffic_record),
            "TCP - http - Attack: False"
        )

    def test_fields_are_populated(self):
        # Test all fields are correctly populated
        self.assertEqual(self.traffic_record.duration, 10)
        self.assertEqual(self.traffic_record.protocol_type, 'TCP')
        self.assertEqual(self.traffic_record.service, 'http')
        self.assertEqual(self.traffic_record.flag, 'SF')
        self.assertEqual(self.traffic_record.src_bytes, 1500)
        self.assertEqual(self.traffic_record.dst_bytes, 3500)
        self.assertFalse(self.traffic_record.land)
        self.assertTrue(self.traffic_record.logged_in)
        self.assertFalse(self.traffic_record.attack)



''' TEST VIEWS
1. Test the NetworkTrafficListView and NetworkTrafficDetailView to verify data is
accurately returned from endpoints
2. Verify that Error handling works as expected '''

class NetworkTrafficViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create sample records
        self.record1 = NetworkTraffic.objects.create(
            duration=2,
            protocol_type='TCP',
            service='http',
            flag='SF',
            src_bytes=500,
            dst_bytes=1000,
            land=False,
            wrong_fragment=0,  # Provide a value for `wrong_fragment`
            urgent=0,
            hot=0,
            logged_in=True,
            num_compromised=0,
            count=1,
            srv_count=1,
            serror_rate=0.0,
            rerror_rate=0.0,
            same_srv_rate=1.0,
            diff_srv_rate=0.0,
            srv_diff_host_rate=0.0,
            dst_host_count=255,
            dst_host_srv_count=255,
            dst_host_same_srv_rate=1.0,
            dst_host_diff_srv_rate=0.0,
            attack=False
        )
        self.record2 = NetworkTraffic.objects.create(
            duration=5,
            protocol_type='UDP',
            service='ftp',
            flag='S0',
            src_bytes=200,
            dst_bytes=400,
            land=False,
            wrong_fragment=0,  # Provide a value for `wrong_fragment`
            urgent=0,
            hot=0,
            logged_in=False,
            num_compromised=0,
            count=1,
            srv_count=1,
            serror_rate=0.0,
            rerror_rate=0.0,
            same_srv_rate=0.5,
            diff_srv_rate=0.0,
            srv_diff_host_rate=0.0,
            dst_host_count=127,
            dst_host_srv_count=127,
            dst_host_same_srv_rate=0.5,
            dst_host_diff_srv_rate=0.0,
            attack=True
        )
        self.valid_id = self.record1.id
        self.invalid_id = 99999

    def test_get_traffic_list(self):
        """Test fetching all traffic records."""
        response = self.client.get('/api/traffic')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['protocol_type'], 'TCP')  # Validate a sample record

    def test_get_traffic_detail_valid(self):
        """Test fetching a single record by valid ID."""
        response = self.client.get(f'/api/traffic/{self.valid_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['protocol_type'], 'TCP')

    def test_get_traffic_detail_invalid(self):
        """Test fetching a single record with an invalid ID."""
        response = self.client.get(f'/api/traffic/{self.invalid_id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Record not found')

