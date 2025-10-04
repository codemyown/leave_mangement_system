from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from .models import LeaveRequest, LeaveBalance , Holiday
from datetime import timedelta
from .helpers import get_working_days, get_active_managers
from .decorators import employee_required , manager_required
from .forms import LeaveRequestForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import date
from fpdf import FPDF
from django.http import HttpResponse

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

@login_required
@employee_required
def leave_history_view(request):
    """
    Display the logged-in employee's leave history and current leave balances.

    - Fetches all leave requests of the user ordered by start date (latest first).
    - Retrieves the user's leave balances.
    - Passes today's date for reference in the template.
    """
    leaves = LeaveRequest.objects.filter(user=request.user).order_by('-start_date')
    balances = LeaveBalance.objects.filter(user=request.user)
    return render(request, 'accounts/leave_history.html', {'leaves': leaves, 'balances': balances, 'today': date.today()})

@login_required
def holiday_calendar_view(request):
    """
    Renders a calendar view of upcoming holidays for the next 30 days.

    Fetches all holidays within the next 30 days from today and maps each date 
    to its holiday name for display in the template.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders 'holiday_calendar.html' template with context 
        containing 'month_days' (list of dates for the next 30 days) and 
        'holiday_dates' (dict mapping holiday dates to names).
    """
    today = date.today()
    month_days = [today + timedelta(days=i) for i in range(30)]
    holidays = Holiday.objects.filter(date__range=[today, today + timedelta(days=30)])
    holiday_dates = {h.date: h.name for h in holidays}

    context = {
        'month_days': month_days,
        'holiday_dates': holiday_dates
    }
    return render(request, 'accounts/holiday_calendar.html', context)

@login_required
@employee_required
def download_leave_history_pdf(request):
    """
    Generate and download a PDF of the logged-in employee's leave history.

    Includes:
    - Leave balances for each leave type.
    - Detailed leave requests with start/end dates, type, status, approver, and reason.

    Returns:
        HttpResponse: PDF file as attachment.
    """
    leaves = LeaveRequest.objects.filter(user=request.user).order_by('-start_date')
    balances = LeaveBalance.objects.filter(user=request.user)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"{request.user.username} - Leave History", ln=True, align="C")
    pdf.ln(10)

    # Leave Balances
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Leave Balances:", ln=True)
    pdf.set_font("Arial", '', 12)
    for bal in balances:
        pdf.cell(0, 8, f"{bal.leave_type.name}: {bal.balance} days", ln=True)
    pdf.ln(5)

    # Leave Requests
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Leave History:", ln=True)
    pdf.set_font("Arial", '', 12)
    for leave in leaves:
        approver_name = leave.approver.username if leave.approver else '-'
        pdf.cell(0, 8, f"{leave.start_date} to {leave.end_date} | {leave.leave_type.name} | {leave.status} | Approver: {approver_name}", ln=True)
        pdf.multi_cell(0, 8, f"Reason: {leave.reason}")
        pdf.ln(2)

    # Output PDF to HttpResponse
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{request.user.username}_leave_history.pdf"'
    pdf.output(dest='F', name=response)
    return response


# Additional views for manager functionalities can be added here.

@login_required
@manager_required
def manager_dashboard_view(request):
    """
    Manager Dashboard View

    Displays pending leave requests that the logged-in manager can approve. 
    Includes leaves where the manager is either the direct approver or has delegated approval authority.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders 'manager_leave_requests.html' with a list of approvable pending leaves.
    """
    today = date.today()
    
    # Get leaves where user is direct manager OR has delegation
    pending_leaves = LeaveRequest.objects.filter(status='Pending')
    
    # Filter leaves current manager can approve
    approvable_leaves = []
    for leave in pending_leaves:
        active_managers = get_active_managers(leave.start_date)
        if request.user in active_managers:
            approvable_leaves.append(leave)
    
    return render(request, 'accounts/manager_leave_requests.html', {'pending_leaves': approvable_leaves})