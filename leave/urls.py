from django.urls import path
from . import views

urlpatterns = [
   path('login/', views.login_view, name='login'),
   path('logout/', views.logout_view, name='logout'),
   path('dashboard/', views.dashboard_view, name='dashboard'),
   path('apply-leave/', views.apply_leave_view, name='apply_leave'),
   path('leave-history/', views.leave_history_view, name='leave_history'),
   path('upcoming-holidays/', views.holiday_calendar_view, name='upcoming_holidays'),
   path('leave-history/download/', views.download_leave_history_pdf, name='download_leave_history_pdf'),
]
