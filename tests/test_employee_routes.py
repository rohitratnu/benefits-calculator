import unittest
from app import create_app, db
from app.models import Employee
from datetime import datetime


class EmployeeRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_all_employees(self):
        response = self.client.get('api/employees')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_create_employee(self):
        response = self.client.post('api/employees/', json={
            'first_name': 'Rohit',
            'last_name': 'Ratnu',
            'date_of_birth': '1980-01-01'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Rohit', response.json['first_name'])

    def test_get_employee_by_id(self):
        employee = Employee(
            first_name='Rohit',
            last_name='Ratnu',
            date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d')
        )
        db.session.add(employee)
        db.session.commit()

        response = self.client.get(f'api/employees/{employee.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Rohit', response.json['first_name'])

    def test_get_employee_benefits_by_id(self):
        employee = Employee(
            first_name='Rohit',
            last_name='Ratnu',
            date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d')
        )
        db.session.add(employee)
        db.session.commit()

        response = self.client.get(f'api/employees/{employee.id}/benefits')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1000, response.json['benefits_cost'])
