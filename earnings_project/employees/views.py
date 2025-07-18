from django.shortcuts import render, redirect
from .models import Employee, SalaryDetail, Expense
from .forms import EmployeeForm, SalaryForm, ExpenseForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


@login_required
def create_employee(request):
    if request.method == "POST":
        emp_form =  EmployeeForm(request.POST)
        salary_form = SalaryForm(request.POST)

        if emp_form.is_valid() and salary_form.is_valid():
            employee = emp_form.save(commit=False)
            employee.user = request.user
            employee.save()

            salary = salary_form.save(commit=False)
            salary.employee = employee
            salary.save()

            return redirect('employee_detail', employee.id)
    else:
        emp_form =  EmployeeForm()
        salary_form = SalaryForm() 
    return render(request, 'employees/create_employee.html',{
        "emp_form":emp_form,
        "salary_form":salary_form
    })

@login_required
def employee_detail(request, pk):
    # get_object_or_404()
    employee = Employee.objects.get(pk=pk)
    salary = SalaryDetail.objects.get(employee=employee)
    expenses = Expense.objects.filter(employee=employee)
    
    # django aggregations and annotations
    total_expenses = sum(e.amount for e in expenses)
    net_income = salary.net_income() - total_expenses
    weekly_income = net_income // (salary.months_worked * 4)

    return render(
        request,
        'employees/employee_detail.html',
        {
            'employee':employee,
            'salary': salary,
            'net_income': net_income,
            'weekly_income': weekly_income,
            'expenses': expenses
        }
    )

    
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
        context = {'form':form}
    return render(request, "registration/register.html",context)