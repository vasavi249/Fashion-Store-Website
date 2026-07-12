from django.urls import path
import views

urlpatterns = [
    # Employees
    path('employees/add/', views.add_employee),
    path('employees/', views.get_employees),
    path('employees/update/<str:id>/', views.update_employee),
    path('employees/delete/<str:id>/', views.delete_employee),
    
    # Departments
    path('departments/add/', views.add_department),
    path('departments/', views.get_departments),
    path('departments/update/<str:id>/', views.update_department),
    path('departments/delete/<str:id>/', views.delete_department),
    
    # Attendance
    path('attendance/add/', views.add_attendance),
    path('attendance/', views.get_attendance),
    path('attendance/update/<str:id>/', views.update_attendance),
    path('attendance/delete/<str:id>/', views.delete_attendance),
    
    # Payroll
    path('payroll/add/', views.add_payroll),
    path('payroll/', views.get_payroll),
    path('payroll/update/<str:id>/', views.update_payroll),
    path('payroll/delete/<str:id>/', views.delete_payroll),
    
    # Payslips
    path('payslips/add/', views.add_payslip),
    path('payslips/', views.get_payslips),
    path('payslips/update/<str:id>/', views.update_payslip),
    path('payslips/delete/<str:id>/', views.delete_payslip),
]
