from django.shortcuts import render
from .models import Employees, Department, Leave_Application
# from .mongo import get_employees_collection
from .serializers import EmployeesSerializer, DepartmentSerializer, LeaveApplicationSerializer
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from django.views import View

# Create your views here.

# class EmployeeView:
#   def get(self,request):
#     employees = Employees.objects.all()
#     departments = Department.objects.all()
#     leave_applications = Leave_Application.objects.all()
    
#     # Fetching data from MongoDB
#     mongo_employees = get_employees_collection().find()

#     context = {
#         'employees': employees,
#         'departments': departments,
#         'leave_applications': leave_applications,
#         'mongo_employees': mongo_employees
#     }
    
#     return render(request, 'employee/employee_list.html', context)
  
#   def post(self, request):
#     # Handle form submission for creating or updating employees
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         base_salary = request.POST.get('baseSalary')
#         department_id = request.POST.get('departmentID')

#         # Create or update employee logic here
#         employee = Employees(name=name, baseSalary=base_salary, departmentID_id=department_id)
#         employee.save()

#         return render(request, 'employee/employee_list.html', {'message': 'Employee saved successfully.'})
    
#     return render(request, 'employee/employee_form.html')
  

# class DepartmentView:
#   def get(self, request):
#     departments = Department.()
#     return render(request, 'employee/department_list.html', {'departments': departments})
  
#   def post(self, request):
#     # Handle form submission for creating or updating departments
#     if request.method == 'POST':
#         name = request.POST.get('name')

#         # Create or update department logic here
#         department = Department(name=name)
#         department.save()

#         return render(request, 'employee/department_list.html', {'message': 'Department saved successfully.'})
    
#     return render(request, 'employee/department_form.html')


class EmployeesListView(ListCreateAPIView):
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializer

class DepartmentListView(ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class LeaveApplicationListView(ListCreateAPIView):
    queryset = Leave_Application.objects.all()
    serializer_class = LeaveApplicationSerializer

class LeaveApplicationView(RetrieveUpdateDestroyAPIView):
    queryset = Leave_Application.objects.all()
    serializer_class = LeaveApplicationSerializer
    lookup_field = 'employeeid'
   


from django.db.models import F, ExpressionWrapper, DecimalField
from rest_framework.generics import ListAPIView

class HighEarnersByDepartmentView(ListAPIView):
    serializer_class = EmployeesSerializer

    def get_queryset(self):
        dept_id = self.kwargs.get("departmentID")  # departmentID passed in URL

        # Step 1: Get top 3 unique base salaries in that department
        top_salaries = (Employees.objects
                        .filter(departmentID=dept_id)
                        .order_by("-baseSalary")
                        .values_list("baseSalary", flat=True)
                        .distinct()[:3])

        # Step 2: Return employees whose baseSalary is in those top salaries
        return Employees.objects.filter(departmentID=dept_id, baseSalary__in=top_salaries)
    
class HighEarnersByMonthView(ListAPIView):
    serializer_class = EmployeesSerializer

    def get_queryset(self):
        month = self.request.query_params.get("month")
        year = self.request.query_params.get("year")

        # Step 1: Annotate payable_salary for each leave record
        qs = (Leave_Application.objects
              .filter(month=month, year=year)
              .annotate(
                  payable_salary=ExpressionWrapper(
                      F("employeeid__baseSalary") -
                      (F("leaves") * (F("employeeid__baseSalary") / 25.0)),
                      output_field=DecimalField(max_digits=10, decimal_places=2)
                  )
              ))

        # Step 2: Get top 3 unique payable salaries
        top_salaries = (qs.order_by("-payable_salary")
                          .values_list("payable_salary", flat=True)
                          .distinct()[:3])

        # Step 3: Return employees who have leave_applications with those salaries
        employees = Employees.objects.filter(
            leave_applications__month=month,
            leave_applications__year=year,
            leave_applications__in=qs.filter(payable_salary__in=top_salaries)
        ).distinct()

        return employees