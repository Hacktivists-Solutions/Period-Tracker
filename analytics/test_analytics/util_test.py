from datetime import date
from django.test import TestCase
from analytics.util import avg_cycle

from tracker.models import MenstrualCycle

class AvgCycleTestCase(TestCase):
    def setUp(self):
        # Create menstrual cycles for testing
        self.cycle1 = MenstrualCycle.objects.create(start_date=date(2022, 1, 1), end_date=date(2022, 1, 5))
        self.cycle2 = MenstrualCycle.objects.create(start_date=date(2022, 1, 10), end_date=date(2022, 1, 15))

    def test_avg_cycle_with_cycles(self):
        # Test when there are multiple menstrual cycles
        menstrual_cycles = MenstrualCycle.objects.all()
        avg = avg_cycle(menstrual_cycles)
        self.assertEqual(avg, 7)  # (5 + 6) / 2 = 5.5

    def test_avg_cycle_with_single_cycle(self):
        # Test when there is only one menstrual cycle
        menstrual_cycles = MenstrualCycle.objects.filter(id=self.cycle1.id)
        avg = avg_cycle(menstrual_cycles)
        self.assertEqual(avg, 5)  # Single cycle of length 5

    def test_avg_cycle_with_no_cycles(self):
        # Test when there are no menstrual cycles
        menstrual_cycles = MenstrualCycle.objects.none()
        avg = avg_cycle(menstrual_cycles)
        self.assertEqual(avg, 0)  # No cycles, so average should be 0
