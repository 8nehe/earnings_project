from django import forms
from .models import Employee, Expense, SalaryDetail

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'age', 'job_title', 'emp_type']

    
class SalaryForm(forms.ModelForm):
    class Meta:
        model =  SalaryDetail
        fields = ['monthly_salary', 'months_worked', 'bonus_percent']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'amount']