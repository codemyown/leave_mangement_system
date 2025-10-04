from django.shortcuts import redirect
from functools import wraps

def employee_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_employee:
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return wrapper

def manager_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_manager:
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return wrapper
