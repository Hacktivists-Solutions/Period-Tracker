from django.contrib.auth.models import User
from django.test import TestCase
from tracker.models import PeriodSymptom, MenstrualCycle
from tracker.serializers import PeriodMenstrualCycle, PeriodSymptomSerializer


class PeriodSymptomSerializerTest(TestCase):
    def setUp(self):
        self.symptom = PeriodSymptom.objects.create(symptom=1)

    def test_period_symptom_serializer(self):
        serializer = PeriodSymptomSerializer(instance=self.symptom)
        expected_data = {
            "symptoms": "Cramps",
            "id": self.symptom.id
        }
        self.assertEqual(serializer.data, expected_data)

