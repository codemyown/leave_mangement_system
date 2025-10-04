from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, LeaveType, LeaveBalance, LeaveRequest, Holiday, Delegation

class CustomUserAdmin(UserAdmin):
    """
    Admin view for custom User model with employee and manager roles.
    """
    model = User
    list_display = ('username', 'email', 'is_employee', 'is_manager', 'department', 'is_staff', 'is_superuser')
    list_filter = ('is_employee', 'is_manager', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_employee', 'is_manager', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'department')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_employee', 'is_manager', 'department', 'is_staff', 'is_superuser')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'annual_quota', 'carry_forward_allowed')
    search_fields = ('name',)

@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'leave_type', 'balance')
    search_fields = ('user__username', 'leave_type__name')

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'leave_type', 'start_date', 'end_date', 'status', 'approver')
    list_filter = ('status', 'leave_type')
    search_fields = ('user__username', 'leave_type__name', 'approver__username')

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    search_fields = ('name',)

@admin.register(Delegation)
class DelegationAdmin(admin.ModelAdmin):
    list_display = ('manager', 'delegate', 'start_date', 'end_date')
    search_fields = ('manager__username', 'delegate__username')

# Register User with custom admin
admin.site.register(User, CustomUserAdmin)
