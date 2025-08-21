from django.urls import path 
from . import views

urlpatterns = [
    path('dept/', views.DepartmentListView.as_view()),
    path('', views.EmployeesListView.as_view()),
    path('leave/', views.LeaveApplicationListView.as_view()),
    path('leave/<int:employeeid>', views.LeaveApplicationView.as_view()),
    path('high/<str:departmentID>', views.HighEarnersByDepartmentView.as_view()),
    path('highMonth/<str:departmentID>/<int:month>', views.HighEarnersByDepartmentView.as_view()),
]
