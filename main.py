from db_utils import (
    create_employee_table,
    save_employee_to_db,
    fetch_employee_from_db,
    update_employee_salary,
    delete_employee,
)

NUMBER_OF_WEEKS = 4

# Polymorphism

class InvalidSalaryData(Exception):
    def __init__(self, salary, months, bonus):
        message = (
            f"Invalid salary data: salary={salary}, months={months}, bonus={bonus}"
        )
        if salary < 0:
            message += " Salary must be non-negative"
        if months <= 0:
            message += " Months must be greater than zero."
        if bonus <= 0:
            message += " Bonus percent must be non-negative"

        super().__init__(message)

class Employee:
    def __init__(self):
        self.details = {}
        self.salary_details = ()
        self.earnings = ()
        self.earner_type = ""
        self.expenses = []
        self.expense_names = set()
        self.weekly_income = 0
        self.balance = 0

    def collect_details(self):
        try:
            self.details["name"] = input("Enter employee's name: ")
            self.details["age"] = input("Enter age: ")
            self.details["job"] = input("Enter job title: ")
        except Exception as e:
            print(f"Error collecting personal details: {e}")

    def collect_salary_info(self):
        try:
            salary = float(input("Enter your monthly salary: "))
            months = int(input("How many months have you worked: "))
            bonus_percent = float(input("Enter your performance bonus (%): "))

            if salary < 0 or months <= 0 or bonus_percent <= 0:
                raise InvalidSalaryData(salary, months, bonus_percent)

            self.salary_details = (salary, months, bonus_percent)
        except ValueError:
            print("Invalid Input! Please enter numeric values.")
            self.collect_salary_info()
        except InvalidSalaryData as e:
            print(f"{e}")
            self.collect_salary_info()
        except Exception as e:
            print(f"Unexpected error during salary input: {e}")
            self.collect_salary_info()

    def calculate_earnings(self):
        try:
            salary, months, bonus_percent = self.salary_details
            total_earnings = salary * months
            bonus_amount = (bonus_percent / 100) * total_earnings
            net_income = total_earnings + bonus_amount
            self.earnings = (total_earnings, bonus_amount, net_income)
        except Exception as e:
            print(f"Error calculatinf earngins: {e}")

    def classify_earner(self):
        try:
            net_income = self.earnings[2]
            if net_income > 1_000_000:
                self.earner_type = "High earner"
            elif net_income > 500_000:
                self.earner_type = "Average earner"
            else:
                self.earner_type = "Low earner"
        except Exception as e:
            print(f"Error collecting expenses: {e}")
            self.classify_earner()

    def collect_expenses(self):
        try:
            self.expenses.clear()
            self.expense_names.clear()

            for i in range(3):
                name = input(f"  Expense #{i + 1} name: ")
                amount = float(input(f" Amount for {name}: "))
                self.expenses.append({"name": name, "amount": amount})
                self.expense_names.add(name)
        except ValueError:
            print(f"Please enter valid numbers for expense amounts.")
            self.collect_expenses()
        except Exception as e:
            print(f" Error colllecting expense: {e}")
            self.collect_expenses()

    def deduct_expenses(self):
        try:
            net_income = self.earnings[2]
            for expense in self.expenses:
                net_income -= expense["amount"]
            self.earnings = (self.earnings[0], self.earnings[1], net_income)
        except Exception as e:
            print(f"Error deducting expenses: {e}")

    def compute_weekly_distribution(self):
        try:
            months = self.salary_details[1]
            net_income = self.earnings[2]
            total_weeks = months * NUMBER_OF_WEEKS

            self.weekly_income = net_income // total_weeks if total_weeks else 0
            self.balance = net_income % total_weeks if total_weeks else net_income
        except Exception as e:
            print(f"Error computing weekly distribution: {e}")

    def print_summary(self):
        try:
            print("\n--- Earnings Summary ---")
            print(f"Name: {self.details['name']}")
            print(f"Age: {self.details['age']}")
            print(f"Job: {self.details['job']}")
            print(f"Monthly Salary: {self.salary_details[0]}")
            print(f"Months worked: {self.salary_details[1]}")
            print(f"Total earnings (Before bonus): {self.earnings[0]}")
            print(f"Bonus Percentage: {self.salary_details[2]}")
            print(f"Bonus Amount: {self.earnings[1]}")
            print(f"Earner Type: {self.earner_type}")
            print(f"Aproximate weekly income: {self.weekly_income}")
            print(f"Balance: {self.balance}")
            print(f"Expenses: {[ expense['name'] for expense in self.expenses ]}")
        except Exception as e:
            print(f"Error printing summary: {e}")
    
    @classmethod
    def from_dict(cls, data):
        """
        Used to create an Employee(or subclass) 
        from a dictionary for deserialization
        """
        obj = cls()
        obj.details = data['details']
        obj.salary_details = tuple(data['salary_details'])
        obj.earnings = tuple(data["earnings"])
        obj.earner_type = data['earner_type']
        obj.expenses = data['expenses']
        obj.expense_names = set(data['expense_names'])
        obj.weekly_income = data['weekly_income']
        obj.balance = data['balance']
        return obj
    
    @staticmethod
    def validate_salary(salary, months, bonus_percent):
        if salary < 0 or months <= 0 or bonus_percent <= 0:
            raise InvalidSalaryData(salary, months, bonus_percent)
    
    def to_dict(self):
        return {
            "details": self.details,
            "salary_details": self.salary_details,
            "earnings": self.earnings,
            "earner_type": self.earner_type,
            "expenses": self.expenses,
            "expense_names": list(self.expense_names),
            "weekly_income": self.weekly_income,
            "balance": self.balance,
        }
    
class FullTimeEmployee(Employee):
    def classify_earner(self):
        net_income = self.earnings[2]
        if net_income > 1_200_000:
            self.earner_type = "Top Full-Time earner"
        elif net_income > 500_000:
            self.earner_type = "Mid Full-Time earner"
        else:
            self.earner_type = "Low Full-Time earner"

class PartTimeEmployee(Employee):
    def classify_earner(self):
        net_income = self.earnings[2]
        if net_income > 600_000:
            self.earner_type = "Top Part-Time earner"
        elif net_income > 300_000:
            self.earner_type = "Mid Part-Time earner"
        else:
            self.earner_type = "Low Part-Time earner"

def save_to_file(employees, filename="employees.json"):
    import json
    with open(filename, "w") as f:
        json.dump([employee.to_dict() for employee in employees], f, indent=2)

def load_from_file(filename="employees.json"):
    import json
    with open(filename, "r") as file:
        data = json.load(file)
        return [Employee.from_dict(employee) for employee in data]

def main():
    create_employee_table()

    add_more = "yes"
    employees = []

    while add_more.lower() == "yes":

        emp_type = input("Enter employee type (full/part/other): ").lower()
        if emp_type == "full":
            emp =  FullTimeEmployee()
        elif emp_type == "part":
            emp = PartTimeEmployee()
        else:
            emp = Employee()

        emp.collect_details()
        emp.collect_salary_info()
        emp.calculate_earnings()
        emp.classify_earner()
        emp.collect_expenses()
        emp.deduct_expenses()
        emp.compute_weekly_distribution()
        # emp.print_summary()

        employees.append(emp)
        save_to_file(employees)
        save_employee_to_db(emp)

        try:
            fetch = input("\n Do you want to fetch an employee? (yes/no): ").lower()
            if fetch == "yes":
                name = input("Enter employee name to fetch: ")
                fetch_employee_from_db(name)

        except Exception as e:
            print(f"Error in fetch input {e}")
            break
        
        add_more = input("\n Do you want to add another employee? (yes/no): ")

    
    
    print("\n All employee data entered. Session completed")

if __name__ == "__main__":
    main()

