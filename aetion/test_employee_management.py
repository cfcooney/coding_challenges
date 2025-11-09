import pytest
from employee_management import Employee, EmployeeDatabase


def test_employee_creation():
    employee = Employee("123456","Ciaran", "Cooney", "Engineering",
                10000.00, "01/01/25")
    assert employee.salary == pytest.approx(10000.00)


def test_negative_salary():
    with pytest.raises(ValueError) as excinfo:
        Employee("123456","Ciaran", "Cooney", "Engineering",
                -10.00, "01/01/25")
    assert "Salary cannot be a negative value." in str(excinfo.value)


def test_empty_department():
    with pytest.raises(ValueError) as excinfo:
        Employee("123456","Ciaran", "Cooney", "",
                -10.00, "01/01/25")
    assert "Department name cannot be empty string." in str(excinfo.value)