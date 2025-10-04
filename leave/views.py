from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

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
