import mysql.connector
import json
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            database=os.environ['DB_NAME']
        )
        print("Connected to database")
        return conn
    except Exception as e:
        print(f"DB Connect Error: {e}")
        return None

def create_employee_table():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees(
                name VARCHAR(100) PRIMARY KEY,
                age VARCHAR(10),
                job VARCHAR(100),
                       salary FLOAT,
                       months INT,
                       bonus_percent FLOAT,
                       total_earnings FLOAT,
                       bonus_amount FLOAT,
                       net_income FLOAT,
                       earner_type VARCHAR(50),
                       weekly_income FLOAT,
                       balance FLOAT,
                       expenses TEXT
            
            )

        """)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error creating table: {e}")

def save_employee_to_db(employee):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM employees WHERE name = %s", (employee.details['name'],) )
        
        if cursor.fetchone():
            print(f"\n[!] Employee `{employee.details['name']}` already exists in the database ")
            return
        
        cursor.execute("""
            INSERT INTO employees(
                name, age, job, salary, months, bonus_percent, total_earnings,
                       bonus_amount, net_income, earner_type, weekly_income, balance, expenses
                ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,(
            employee.details['name'],
            employee.details['age'],
            employee.details['job'],
            employee.salary_details[0],
            employee.salary_details[1],
            employee.salary_details[2],
            employee.earnings[0],
            employee.earnings[1],
            employee.earnings[2],
            employee.earner_type,
            employee.weekly_income,
            employee.balance,
            json.dumps(employee.expenses),
        ),)
        conn.commit()
        print(f"\n[!] Employee '{employee.details['name']}' saved to the database")

    except Exception as e:
        print(f"Error saving to DB: {e}")
    finally:
        conn.close()

def fetch_employee_from_db(name):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employees WHERE name = %s", (name,))
            row = cursor.fetchone()
            if not row:
                print("Employee not found")
                return None
            
            print("\n---- Employee from Database ---")
            for key, value in row:
                print(f"{key}: {value}")

            return row
        except Exception as e:
            print(f"Error saving to DB: {e}")
        finally:
            conn.close()

def update_employee_salary(new_salary, name):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE employees  SET salary = %s WHERE name = %s", (new_salary,name))
            conn.commit()
  
            print("\n---- Employee Updated ---")
        except Exception as e:
            print(f"Error updating employee: {e}")
        finally:
            conn.close()

def delete_employee(name):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM employees WHERE name = %s", (name,))
            conn.commit()
  
            print("\n---- Employee Deleted ---")
        except Exception as e:
            print(f"Error deleting employee: {e}")
        finally:
            conn.close()