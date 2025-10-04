from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from .models import LeaveRequest, LeaveBalance
from .helpers import get_working_days, get_active_managers
from .decorators import employee_required
from .forms import LeaveRequestForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

def login_view(request):
    """
    Handle user login.

    POST: Authenticate and log in the user, then redirect to 'dashboard'.
    GET: Render the login page.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        return render(request, 'accounts/login.html', {'error': 'Invalid username or password'})

    return render(request, 'accounts/login.html')


@login_required
def dashboard_view(request):
    """
    Render dashboard based on user role.

    - Employee: show employee dashboard.
    - Manager: redirect to manager dashboard.
    - Others: redirect to login page.
    """
    user = request.user
    if user.is_employee:
        return render(request, 'accounts/employee_dashboard.html')
    elif user.is_manager:
        return redirect('manager_dashboard')
    return redirect('login')


def logout_view(request):
    """
    Log out the current user and redirect to the login page.
    """
    logout(request)
    return redirect('login')

@login_required
@employee_required
def apply_leave_view(request):
    """
    Allow an employee to apply for leave.

    - Validates leave request form on POST.
    - Checks leave balance for the selected leave type.
    - Prevents overlapping approved leaves.
    - Saves leave request with 'Pending' status.
    - Sends email notifications to active managers considering delegation.
    - Displays leave application form on GET request.
    """
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_type = form.cleaned_data['leave_type']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            working_days = get_working_days(start_date, end_date)
            total_working_days = len(working_days)

            balance_obj = LeaveBalance.objects.filter(user=request.user, leave_type=leave_type).first()
            if not balance_obj or balance_obj.balance < total_working_days:
                messages.error(request, f'Insufficient leave balance (working days: {total_working_days}).')
                return redirect('apply_leave')

            overlapping = LeaveRequest.objects.filter(
                user=request.user,
                status='Approved',
                start_date__lte=end_date,
                end_date__gte=start_date
            )
            if overlapping.exists():
                messages.error(request, "You already have approved leave during this period.")
                return redirect('apply_leave')

            leave = form.save(commit=False)
            leave.user = request.user
            leave.status = 'Pending'
            leave.save()

            active_managers = get_active_managers(start_date)
            for manager in active_managers:
                send_mail(
                    subject=f"New Leave Request from {request.user.username}",
                    message=f"{request.user.username} applied for {leave_type.name} from {start_date} to {end_date} ({total_working_days} working days).",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[manager.email],
                )

            messages.success(request, f'Leave request submitted ({total_working_days} working days).')
            return redirect('apply_leave')
    else:
        form = LeaveRequestForm()
    return render(request, 'accounts/apply_leave.html', {'form': form})