from django.core.management.base import BaseCommand
from leave.models import User, LeaveType, LeaveBalance
from datetime import date

class Command(BaseCommand):
    help = 'Auto-credit leave balances monthly/yearly'

    def handle(self, *args, **kwargs):
        today = date.today()

        # Monthly leave credit
        monthly_leave_types = LeaveType.objects.filter(name__in=['Casual', 'Earned'])  
        for leave_type in monthly_leave_types:
            for user in User.objects.filter(is_employee=True):
                balance_obj, created = LeaveBalance.objects.get_or_create(user=user, leave_type=leave_type)
                balance_obj.balance += 1  
                balance_obj.save()
                self.stdout.write(f'Credited 1 {leave_type.name} leave to {user.username}')

        # Yearly leave credit
        if today.month == 1 and today.day == 1:  # every Jan 1
            yearly_leave_types = LeaveType.objects.filter(name__in=['Sick'])
            for leave_type in yearly_leave_types:
                for user in User.objects.filter(is_employee=True):
                    balance_obj, created = LeaveBalance.objects.get_or_create(user=user, leave_type=leave_type)
                    balance_obj.balance = leave_type.annual_quota  # reset/add yearly
                    balance_obj.save()
                    self.stdout.write(f'Credited yearly {leave_type.name} leave to {user.username}')
