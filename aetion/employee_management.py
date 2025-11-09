# Employee Management System
import json
import os
import uuid
from datetime import datetime

class Employee:
    RATING_LOWER_BOUND = 1
    RATING_UPPER_BOUND = 5

    def __init__(self, emp_id: str, first_name:str, last_name: str, department: str,
                salary: float, hire_date: datetime):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        if department == "":
            raise ValueError("Department name cannot be empty string.")
        self.department = department
        if salary < 0.0:
            raise ValueError("Salary cannot be a negative value.")
        self.salary = salary
        self.hire_date = hire_date
        self.performance_ratings = []
        self.rating_low = self.RATING_LOWER_BOUND
        self.rating_high = self.RATING_UPPER_BOUND

    
    def get_full_name(self) -> str:
        """Returns the full name of the employee."""
        return f"{self.first_name} {self.last_name}"
    
    def add_performance_rating(self, rating: float, review_date: datetime):
        """Append performance rating to employee profile."""
        if rating >= self.rating_low and rating <= self.rating_high:
            self.performance_ratings.append({'rating': rating, 'date': review_date})
        else:
            raise ValueError("Invalid rating. Must be between 1 and 5.")
    
    def get_average_rating(self) -> float:
        """Compute average rating from employee."""
        if len(self.performance_ratings) == 0:
            return 0
        total = 0
        for rating_entry in self.performance_ratings:
            total += rating_entry['rating']
        return total / len(self.performance_ratings)
    
    def give_raise(self, percentage: float) -> None:
        """Apply percentation increase to employee salary."""
        if not isinstance(percentage, float):
            raise ValueError(f"Input percentage must be a float, not type {type(percentage)}.")
        self.salary += (self.salary * percentage / 100)
        

class EmployeeDatabase:
    def __init__(self, filename: str):
        self.filename = filename
        self.employees = {}
        self.load_employees()
    
    def load_employees(self) -> None:
        """Load employees to the database."""
        if not os.path.exists(self.filename):
            raise FileNotFoundError(f"File name {self.filename} does not exist")
        
        with open(self.filename, 'r') as f:
            data = json.load(f)
            for emp_data in data:
                try:
                    # Validate required fields exist
                    required_fields = ['emp_id', 'first_name', 'last_name', 'department', 'salary', 'hire_date']
                    missing_fields = [field for field in required_fields if field not in emp_data]
                    if missing_fields:
                        raise ValueError(f"Missing required fields: {missing_fields}")
                    
                    # Validate employee ID
                    if not isinstance(emp_data['emp_id'], str) or not emp_data['emp_id'].strip():
                        raise ValueError("Employee ID must be a non-empty string")
                    
                    # Check for duplicate employee ID
                    if emp_data['emp_id'] in self.employees:
                        raise ValueError(f"Employee ID {emp_data['emp_id']} already exists")
                    
                    # Validate salary
                    if not isinstance(emp_data['salary'], (int, float)) or emp_data['salary'] < 0:
                        raise ValueError(f"Invalid salary: {emp_data['salary']}. Must be a positive number")
                    
                    emp = Employee(
                        emp_data['emp_id'],
                        emp_data['first_name'],
                        emp_data['last_name'],
                        emp_data['department'],
                        emp_data['salary'],
                        emp_data['hire_date']
                    )
                    emp.performance_ratings = emp_data.get('performance_ratings', [])
                    self.employees[emp.emp_id] = emp
                    
                except (ValueError, TypeError, KeyError) as e:
                    # Raise exception instead of just printing
                    raise ValueError(f"Failed to load employee {emp_data.get('emp_id', 'UNKNOWN')}: {str(e)}")
                except Exception as e:
                    # Handle unexpected errors
                    raise RuntimeError(f"Unexpected error loading employee {emp_data.get('emp_id', 'UNKNOWN')}: {str(e)}")
    
    def save_employees(self) -> None:
        """Save the employee database as a json object."""
        try:
            emp_list = []
            for _, emp in self.employees.items():
                emp_dict = {
                    'emp_id': emp.emp_id,
                    'first_name': emp.first_name,
                    'last_name': emp.last_name,
                    'department': emp.department,
                    'salary': emp.salary,
                    'hire_date': emp.hire_date,
                    'performance_ratings': emp.performance_ratings
                }
                emp_list.append(emp_dict)
            
            with open(self.filename, 'w') as f:
                json.dump(emp_list, f, indent=2)
        except Exception:
            raise Exception("Error saving employee data")
    
    def add_employee(self, emp_id: str, first_name: str, last_name: str, department: str,
                      salary: float, hire_date: datetime) -> None:
        """Add new employee to the database."""
        if emp_id in self.employees:
            raise ValueError("Employee ID {emp_id} already exists")
        
        new_emp = Employee(emp_id, first_name, last_name, department, salary, hire_date)
        self.employees[emp_id] = new_emp
        self.save_employees()
    
    def remove_employee(self, emp_id) -> None:
        """remove employee from the database."""
        if not isinstance(emp_id, str) or emp_id not in self.employees:
            raise ValueError("Cannot perform remove employee")
        
        del self.employees[emp_id]
        self.save_employees()

    def get_employee(self, emp_id: str) -> Employee:
        """Return employee details."""
        if not isinstance(emp_id, str) or emp_id not in self.employees:
            raise ValueError("Cannot perform get employee")
        return self.employees[emp_id]
    
    def _get_employees_by_department(self, department: str) -> list:
        """Return employees by department."""
        return [emp for _, emp in self.employees.items() if emp.department == department]
    
    def get_average_salary_by_department(self, department: str) -> float:
        """Return average salary by company department."""
        employees = self._get_employees_by_department(department)
        if not employees:
            return 0.0        
        total_salary = 0
        for emp in employees:
            total_salary += emp.salary
        return total_salary / len(employees)
    
    def get_top_performers(self, min_rating) -> list:
        """Return top performers based on average rating."""
        top_performers = [{'emp': emp, 'avg_rating': emp.get_average_rating()} for _, emp in self.employees.items() if emp.get_average_rating() > min_rating]
        return top_performers

if __name__ == '__main__':
    # Example usage
    db = EmployeeDatabase("employees.json")
    db.add_employee(str(uuid.uuid4()), "John", "Doe", "Engineering", 75000, "2022-01-15")
    db.add_employee(str(uuid.uuid4()), "Jane", "Smith", "Marketing", 65000, "2022-03-01")

    emp = db.get_employee("E001")
    if emp:
        emp.add_performance_rating(4.5, "2023-01-15")
        emp.add_performance_rating(4.8, "2023-07-15")
        print(f"Average rating for {emp.get_full_name()}: {emp.get_average_rating()}")

"""
REFACTORING REVIEW - EMPLOYEE MANAGEMENT SYSTEM
===============================================

THINGS DONE WELL:
-----------------

1. **Constants Implementation** ✅
   - Added RATING_LOWER_BOUND and RATING_UPPER_BOUND class constants
   - Used them in __init__ as instance variables (rating_low, rating_high)
   - This eliminates magic numbers and makes validation bounds configurable

2. **Type Hinting Improvements** ✅
   - Added return type hints to most methods (str, float, None, list, Employee)
   - Added parameter type hints for key methods (rating: float, emp_id: str, etc.)
   - Shows good understanding of Python typing best practices

3. **Documentation Enhancement** ✅
   - Added docstrings to all methods with clear, concise descriptions
   - Docstrings explain what each method does in plain English
   - Consistent docstring format throughout the codebase

4. **Exception Handling Improvements** ✅
   - Replaced print statements with proper ValueError exceptions
   - Added specific error messages with context
   - Used ValueError and FileExistsError appropriately for different error types

5. **Input Validation** ✅
   - Added type checking in give_raise() method
   - Added validation in remove_employee() and get_employee()
   - Shows defensive programming approach

6. **Import Organization** ✅
   - Added uuid import for better employee ID generation
   - Clean, organized import structure at the top

7. **Method Visibility** ✅
   - Made _get_employees_by_department() private with underscore prefix
   - Shows understanding of encapsulation principles

AREAS NEEDING ATTENTION:
-----------------------

1. **Runtime Errors** ❌ CRITICAL
   - Line 79: `self.employees.get_items()` - should be `self.employees.items()`
   - Line 126: `self.employees.get_items()` - same issue
   - Line 132: `self.employees.get_item()` - should be `self.employees.items()`
   - These will cause AttributeError at runtime

2. **Incomplete Type Hinting** ⚠️
   - Missing type hints in __init__ methods for both classes
   - get_top_performers() missing parameter type hint for min_rating
   - Some parameters still lack type annotations

3. **Inconsistent Error Handling** ⚠️
   - Line 65: Still has print() statement instead of exception
   - Line 90: Generic Exception instead of specific exception type
   - Mixed approach between exceptions and print statements

4. **Logic Issues** ⚠️
   - Line 54: FileExistsError used incorrectly (should be FileNotFoundError)
   - Line 98: f-string formatting missing in error message
   - UUID usage in example might not match existing employee IDs

5. **Missing Validation** ⚠️
   - No validation for salary (could be negative)
   - No validation for department names (empty strings)
   - No validation for rating bounds in constructor vs method

6. **Efficiency Opportunities** ⚠️
   - get_average_rating() could use sum() and len() instead of manual loop
   - get_average_salary_by_department() could use list comprehension + sum()
   - Multiple iterations in some methods could be optimized

OVERALL ASSESSMENT:
------------------
🟢 **Strengths**: Excellent work on constants, type hints, docstrings, and most exception handling
🟡 **Priority Fixes**: Fix the .get_items()/.get_item() method calls (will crash)
🔴 **Next Steps**: Complete type hinting, consistent error handling, and add comprehensive validation

Your refactoring shows strong understanding of Python best practices and you've made substantial improvements to code quality, maintainability, and documentation. The main issues are runtime bugs that need immediate attention.
"""