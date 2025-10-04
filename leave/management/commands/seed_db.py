from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from leave.models import LeaveType, LeaveBalance, Holiday, Delegation
from datetime import date, timedelta

User = get_user_model()

class Command(BaseCommand):  # <-- MUST be named Command
    help = 'Seed the database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        # --- Users ---
        if not User.objects.filter(username='manager').exists():
            User.objects.create_user(username='manager', password='manager', is_manager=True, department='HR')
        if not User.objects.filter(username='emp').exists():
            User.objects.create_user(username='emp1', password='emp123', is_employee=True, department='HR')
        if not User.objects.filter(username='emp').exists():
            User.objects.create_user(username='emp', password='emp', is_employee=True, department='IT')

        self.stdout.write("Users created.")

        # --- Leave Types ---
        sick = LeaveType.objects.get_or_create(name='Sick', annual_quota=12, carry_forward_allowed=True)[0]
        casual = LeaveType.objects.get_or_create(name='Casual', annual_quota=10, carry_forward_allowed=False)[0]
        earned = LeaveType.objects.get_or_create(name='Earned', annual_quota=15, carry_forward_allowed=True)[0]

        self.stdout.write("Leave types created.")

        # --- Leave Balances ---
        for user in User.objects.filter(is_employee=True):
            for leave_type in [sick, casual, earned]:
                LeaveBalance.objects.get_or_create(user=user, leave_type=leave_type, balance=leave_type.annual_quota)

        self.stdout.write("Leave balances created.")

        # --- Holidays ---
        for i in range(3):
            hol_date = date.today() + timedelta(days=i+1)
            Holiday.objects.get_or_create(date=hol_date, name=f"Holiday {i+1}")

        self.stdout.write("Holidays created.")

        # --- Delegation ---
        manager = User.objects.get(username='manager1')
        delegate = User.objects.get(username='emp1')
        Delegation.objects.get_or_create(manager=manager, delegate=delegate,
                                       start_date=date.today(),
                                       end_date=date.today() + timedelta(days=7))

        self.stdout.write("Delegation created.")
        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
