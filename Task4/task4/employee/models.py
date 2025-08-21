from django.db import models

# Create your models here.
class Employees(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=50)
  baseSalary = models.IntegerField(default=0)
  departmentID = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='employees')

  def __str__(self):
    return self.name
  
class Department(models.Model):
  id = models.UUIDField(primary_key=True)
  name = models.CharField(max_length=50)

  def __str__(self):
    return self.name 
  

class Leave_Application(models.Model):
  employeeid = models.ForeignKey(Employees, on_delete=models.CASCADE, related_name='leave_applications')
  month = models.CharField(max_length=20)
  year = models.CharField(max_length=4)
  leaves = models.IntegerField(default=0)

  def __str__(self):
    return self.employeeid.name
  
  @property
  def payable_salary(self):
      base_salary = self.employeeid.baseSalary
      deduction = self.leaves * (base_salary / 25)
      return base_salary - deduction  