from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from leave.models import User, LeaveType, LeaveBalance, Holiday, LeaveRequest, Delegation
from datetime import date

class Command(BaseCommand):
    help = 'Populate sample test data for leave management'

    def handle(self, *args, **options):
        User = get_user_model()

        # Create Leave Types
        LeaveType.objects.get_or_create(name='Annual Leave', defaults={'annual_quota': 12, 'carry_forward_allowed': True})
        LeaveType.objects.get_or_create(name='Sick Leave', defaults={'annual_quota': 10, 'carry_forward_allowed': False})
        self.stdout.write(self.style.SUCCESS('Leave types created'))

        # Create Users
        ajay, _ = User.objects.get_or_create(username='ajay', defaults={'email': 'ajay@example.com', 'is_employee': True, 'department': 'IT'})
        ajay.set_password('ajay')
        ajay.save()

        vijay, _ = User.objects.get_or_create(username='vijay', defaults={'email': 'vijay@example.com', 'is_manager': True, 'department': 'HR'})
        vijay.set_password('vijay')
        vijay.save()

        admin, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True, 'department': 'Admin'})
        admin.set_password('admin')
        admin.is_superuser = True  # Ensure superuser
        admin.save()
        self.stdout.write(self.style.SUCCESS('Users created: ajay/ajay (employee), vijay/vijay (manager), admin/admin (superuser)'))

        # Create Balances for ajay
        lt_annual = LeaveType.objects.get(name='Annual Leave')
        lt_sick = LeaveType.objects.get(name='Sick Leave')
        LeaveBalance.objects.get_or_create(user=ajay, leave_type=lt_annual, defaults={'balance': 12})
        LeaveBalance.objects.get_or_create(user=ajay, leave_type=lt_sick, defaults={'balance': 10})
        self.stdout.write(self.style.SUCCESS('Balances created for ajay'))

        # Create Holidays
        Holiday.objects.get_or_create(date=date(2025, 10, 20), defaults={'name': 'Diwali'})
        Holiday.objects.get_or_create(date=date(2025, 12, 25), defaults={'name': 'Christmas'})
        Holiday.objects.get_or_create(date=date(2026, 1, 1), defaults={'name': 'New Year'})
        self.stdout.write(self.style.SUCCESS('Holidays created'))

        # Create Leave Request for ajay
        LeaveRequest.objects.get_or_create(
            user=ajay, leave_type=lt_annual, start_date=date(2025, 11, 1),
            end_date=date(2025, 11, 5), defaults={'reason': 'Vacation', 'status': 'Pending'}
        )
        self.stdout.write(self.style.SUCCESS('Leave request created for ajay'))

        # Create Delegation
        Delegation.objects.get_or_create(
            manager=vijay, delegate=ajay, start_date=date(2025, 10, 1),
            end_date=date(2025, 10, 31)
        )
        self.stdout.write(self.style.SUCCESS('Delegation created: vijay to ajay'))

        self.stdout.write(self.style.SUCCESS('All sample data added!'))