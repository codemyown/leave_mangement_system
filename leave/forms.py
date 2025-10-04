from django import forms
from .models import LeaveRequest

class LeaveRequestForm(forms.ModelForm):
    """
    Form for employees to submit leave requests.

    Fields:
        - leave_type: Type of leave.
        - start_date: Start date of leave.
        - end_date: End date of leave.
        - reason: Reason for the leave.

    Widgets:
        - Date fields use HTML5 date input.
        - Reason uses a textarea with 3 rows.
        - Leave type uses a styled select dropdown.
    """
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'end_date': forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'reason': forms.Textarea(attrs={'rows':3,'class':'form-control'}),
            'leave_type': forms.Select(attrs={'class':'form-select'})
        }
