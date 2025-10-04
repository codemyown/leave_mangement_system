from datetime import date, timedelta
from django.db.models import Sum
from .models import Holiday, User, Delegation

def get_working_days(start_date, end_date):
    """
    Calculate working days between start_date and end_date, excluding holidays.

    Args:
        start_date (date): Start of the period.
        end_date (date): End of the period.

    Returns:
        List[date]: List of working days excluding holidays.
    """
    all_days = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    holidays = set(h.date for h in Holiday.objects.filter(date__range=[start_date, end_date]))
    working_days = [day for day in all_days if day not in holidays]
    return working_days


def get_active_managers(target_date=None):
    """
    Returns a list of managers who can approve leaves on the given date.
    If a manager has delegated authority, the delegate is returned instead.

    Args:
        target_date (date, optional): Date to check for active managers. Defaults to today.

    Returns:
        List[User]: List of active managers or delegates for the target date.
    """
    if target_date is None:
        target_date = date.today()
    
    active_managers = []
    all_managers = User.objects.filter(is_manager=True)
    
    for manager in all_managers:
        delegation = Delegation.objects.filter(
            manager=manager,
            start_date__lte=target_date,
            end_date__gte=target_date
        ).first()
        
        if delegation:
            active_managers.append(delegation.delegate)
        else:
            active_managers.append(manager)
    
    return list(set(active_managers)) 
