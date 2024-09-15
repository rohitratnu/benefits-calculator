# tests/test_employee.py
import unittest
from datetime import datetime

from app import create_app, db
from app.models import Employee


class EmployeeTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_employee(self):
        data = {'first_name': 'John', 'last_name': 'Doe', 'date_of_birth': '1990-01-01'}
        employee = Employee(first_name=data['first_name'],
                            last_name=data['last_name'],
                            date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d'))
        db.session.add(employee)
        db.session.commit()
        self.assertIsNotNone(employee.id)


if __name__ == '__main__':
    unittest.main()
