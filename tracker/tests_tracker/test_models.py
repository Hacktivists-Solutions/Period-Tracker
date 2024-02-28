from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date

from tracker.admin import PeriodSymptomAdmin
from tracker.models import MenstrualCycle, PeriodSymptom


class PeriodSymptomModelTest(TestCase):
    def test_create_period_symptom(self):
        symptom = PeriodSymptom.objects.create(symptom=1)
        self.assertIsInstance(symptom, PeriodSymptom)
        self.assertEqual(symptom.get_symptom_display(), "Cramps")


class MenstrualCycleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.cycle = MenstrualCycle.objects.create(user=self.user, start_date=date(2024, 1, 1), end_date=date(2024, 1, 5))

    def test_create_menstrual_cycle(self):
        self.assertIsInstance(self.cycle, MenstrualCycle)
        self.assertEqual(self.cycle.user, self.user)
        self.assertEqual(self.cycle.start_date, date(2024, 1, 1))
        self.assertEqual(self.cycle.end_date, date(2024, 1, 5))

    def test_cycle_duration(self):
        self.assertEqual(self.cycle.duration(), 5)
