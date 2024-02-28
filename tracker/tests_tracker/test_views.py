from datetime import date
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

from tracker.models import MenstrualCycle
 


class MenstrualCycleTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.client.force_authenticate(user=self.user)

    def test_record_menstrual_cycle(self):
        url = reverse('record_cycle')
        data = {
            "start_date": "2024-01-01",
            "end_date": "2024-01-05",
            "symptoms": [{"symptom": 1}, {"symptom": 2}]  
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MenstrualCycle.objects.count(), 1)
        menstrual_cycle = MenstrualCycle.objects.first()
        self.assertEqual(menstrual_cycle.user, self.user)
        self.assertEqual(menstrual_cycle.start_date, date(2024, 1, 1))
        self.assertEqual(menstrual_cycle.end_date, date(2024, 1, 5))

    def test_get_menstrual_cycles(self):
        MenstrualCycle.objects.create(user=self.user, start_date=date(2024, 1, 1), end_date=date(2024, 1, 5))
        url = reverse('get_cycles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_menstrual_cycles(self):
        MenstrualCycle.objects.create(user=self.user, start_date=date(2024, 1, 1), end_date=date(2024, 1, 5))
        url = reverse('filter_cycles')
        data = {
            "start_date": "2024-01-01",
            "end_date": "2024-01-05",
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

