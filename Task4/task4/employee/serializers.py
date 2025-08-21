from rest_framework import serializers
from .models import Employees, Department, Leave_Application

class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'    


class LeaveApplicationSerializer(serializers.ModelSerializer):
    payable_salary = serializers.SerializerMethodField()
    def get_payable_salary(self, obj):
        return obj.payable_salary

    class Meta:
        model = Leave_Application
        fields = '__all__'

