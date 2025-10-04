from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model extending AbstractUser.

    Attributes:
        is_employee (bool): Flag to indicate if the user is an employee.
        is_manager (bool): Flag to indicate if the user is a manager.
        department (str): Optional department name for the user.
    """
    is_employee = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    department = models.CharField(max_length=100, blank=True, null=True)



class LeaveType(models.Model):
    """
    Model representing types of leaves.

    Attributes:
        name (str): Name of the leave type.
        annual_quota (int): Number of leave days allocated per year (default 12).
        carry_forward_allowed (bool): Whether unused leaves can be carried forward.
    """
    name = models.CharField(max_length=50)
    annual_quota = models.IntegerField(default=12)
    carry_forward_allowed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class LeaveBalance(models.Model):
    """
    Model representing the leave balance for a user per leave type.

    Attributes:
        user (User): Reference to the user.
        leave_type (LeaveType): Type of leave.
        balance (int): Number of remaining leave days (default 0).
    """
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    leave_type = models.ForeignKey('LeaveType', on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.leave_type.name}: {self.balance}"


class Holiday(models.Model):
    """
    Model representing a holiday.

    Attributes:
        date (DateField): Unique date of the holiday.
        name (str): Name/description of the holiday.
    """
    date = models.DateField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.date})"


class LeaveRequest(models.Model):
    """
    Model representing a leave request made by a user.

    Attributes:
        STATUS_CHOICES (tuple): Possible statuses for a leave request.
        user (User): User requesting the leave.
        leave_type (LeaveType): Type of leave requested.
        start_date (DateField): Start date of the leave.
        end_date (DateField): End date of the leave.
        reason (TextField): Reason for the leave.
        status (str): Current status of the leave request (default 'Pending').
        approver (User): Manager or approver of the leave (optional).
        comments (TextField): Additional comments from approver (optional).
    """
    STATUS_CHOICES = (
        ('Pending', 'Pending'), 
        ('Approved', 'Approved'), 
        ('Rejected', 'Rejected'),
        ('Cancelled', 'Cancelled')
    )

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    leave_type = models.ForeignKey('LeaveType', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    approver = models.ForeignKey('User', related_name='approver', on_delete=models.SET_NULL, null=True, blank=True)
    comments = models.TextField(blank=True, null=True)

    @property
    def total_days(self):
        """Calculate total number of leave days including start and end date."""
        return (self.end_date - self.start_date).days + 1

    def __str__(self):
        return f"{self.user.username} - {self.leave_type.name} ({self.status})"
