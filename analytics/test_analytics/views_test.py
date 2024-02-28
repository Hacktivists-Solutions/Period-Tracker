from datetime import datetime, timedelta
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from tracker.models import MenstrualCycle, PeriodSymptom

class AvgCycleLengthTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.cycle1 = MenstrualCycle.objects.create(user=self.user, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=5))
        self.cycle2 = MenstrualCycle.objects.create(user=self.user, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=7))

    def test_avg_cycle_length(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get(reverse('avg_cycle_length'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['avg_cycle'], 6)  # Average of (5+7)/2 = 6 days

class PredictFuturePeriodsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.cycle1 = MenstrualCycle.objects.create(user=self.user, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=28))

    def test_predict_future_periods_view(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get(reverse('predict_future_periods'))
        self.assertEqual(response.status_code, 200)
        expected_date = (datetime.now() + timedelta(days=28)).strftime('%Y-%m-%d')
        self.assertEqual(response.data['next_period_date'], expected_date)

class IdentifySymptomPatternsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.symptom1 = PeriodSymptom.objects.create(symptom='Cramps')
        self.symptom2 = PeriodSymptom.objects.create(symptom='Mood Swings')
        self.cycle1 = MenstrualCycle.objects.create(user=self.user)
        self.cycle1.symptoms.add(self.symptom1)
        self.cycle2 = MenstrualCycle.objects.create(user=self.user)
        self.cycle2.symptoms.add(self.symptom2)

    def test_identify_symptom_patterns(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get(reverse('identify_symptom_patterns'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['symptom_patterns']), 2)  # Two distinct symptoms
