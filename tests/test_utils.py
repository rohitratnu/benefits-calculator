import unittest
from app.models import Employee, Dependent
from app.utils import calculate_benefits_cost
from datetime import datetime


class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        # Create an employee and dependents for testing
        self.employee = Employee(
            first_name='Rohit',
            last_name='Ratnu',
            date_of_birth=datetime.strptime('1980-01-01', '%Y-%m-%d')
        )
        self.dependent1 = Dependent(
            first_name='Wife fname',
            last_name='Wife lname',
            relationship='Spouse',
            date_of_birth=datetime.strptime('1985-01-01', '%Y-%m-%d'),
            employee=self.employee
        )
        self.dependent2 = Dependent(
            first_name='Alice',
            last_name='Ratnu',
            relationship='Child',
            date_of_birth=datetime.strptime('2010-01-01', '%Y-%m-%d'),
            employee=self.employee
        )
        self.employee.dependents = [self.dependent1, self.dependent2]

    def test_calculate_benefits_cost(self):
        # Test the benefits cost calculation
        cost = calculate_benefits_cost(self.employee)
        expected_cost = 1000 + 500 + (500 * 0.9)  # Employee + Dependent1 + Dependent2 with discount
        self.assertEqual(cost, expected_cost)

    def test_calculate_benefits_cost_with_discount(self):
        # Test the benefits cost calculation with employee discount
        self.employee.first_name = 'Alice'
        cost = calculate_benefits_cost(self.employee)
        expected_cost = 1000 * 0.9 + 500 + (500 * 0.9)  # Employee with discount + Dependent1 + Dependent2 with discount
        self.assertEqual(cost, expected_cost)
