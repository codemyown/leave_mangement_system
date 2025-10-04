from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

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
