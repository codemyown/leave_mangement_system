from django.test import TestCase
from datetime import date, timedelta
from leave.helpers import get_working_days
from leave.models import Holiday, LeaveRequest, LeaveType, User

class LeaveCalculationTests(TestCase):

    def test_get_working_days_no_holidays(self):
        start = date(2025, 10, 1)
        end = date(2025, 10, 3)
        days = get_working_days(start, end)
        self.assertEqual(len(days), 3)

    def test_get_working_days_with_holiday(self):
        start = date(2025, 10, 1)
        end = date(2025, 10, 3)
        Holiday.objects.create(date=date(2025, 10, 2), name='Test Holiday')
        days = get_working_days(start, end)
        self.assertEqual(len(days), 2)  

    def test_get_working_days_weekend(self):
        start = date(2025, 10, 4)  
        end = date(2025, 10, 6)    
        days = get_working_days(start, end)
        self.assertEqual(len(days), 3)  

    def test_get_working_days_single_day(self):
        start = end = date(2025, 10, 5)
        days = get_working_days(start, end)
        self.assertEqual(len(days), 1)

    def test_leave_request_total_days(self):
        user = User.objects.create_user(username='test', password='testpass')
        leave_type = LeaveType.objects.create(name='Annual')
        req = LeaveRequest.objects.create(
            user=user, leave_type=leave_type,
            start_date=date(2025, 10, 1),
            end_date=date(2025, 10, 3),
            reason='Test'
        )
        self.assertEqual(req.total_days, 3)