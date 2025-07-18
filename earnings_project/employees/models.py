from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    EMP_TYPE_CHOICES = [
        ('full', 'Full Time'),
        ('part', 'Part Time'),
        ('other', 'other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    job_title = models.CharField(max_length=100)
    emp_type = models.CharField(max_length=100, choices=EMP_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.job_title})"

class SalaryDetail(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    monthly_salary = models.FloatField()
    months_worked = models.PositiveIntegerField()
    bonus_percent = models.FloatField()

    def total_earnings(self):
        return self.monthly_salary * self.months_worked
    
    def bonus_amount(self):
        return (self.bonus_percent / 100) * self.total_earnings()
    
    def net_income(self):
        return self.total_earnings() + self.bonus_amount()


class Expense(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='expenses')
    name = models.CharField(max_length=100)
    amount = models.FloatField()
