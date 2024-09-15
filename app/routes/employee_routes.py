from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from datetime import datetime
from ..models import db, Employee, Dependent
from ..utils import calculate_benefits_cost

ns = Namespace('employees', description='Employee operations')

employee_model = ns.model('Employee', {
    'id': fields.Integer(readonly=True, description='The unique identifier of the employee'),
    'first_name': fields.String(required=True, description='First name of the employee'),
    'last_name': fields.String(required=True, description='Last name of the employee'),
    'salary': fields.Float(description='Salary of the employee'),
    'date_of_birth': fields.Date(required=True, description='Date of birth of the employee'),
    'dependents': fields.List(fields.Nested(ns.model('Dependent', {
        'id': fields.Integer(readonly=True, description='The unique identifier of the dependent'),
        'first_name': fields.String(required=True, description='First name of the dependent'),
        'last_name': fields.String(required=True, description='Last name of the dependent'),
        'relationship': fields.String(required=True, description='Relationship to the employee'),
        'date_of_birth': fields.Date(required=True, description='Date of birth of the dependent')
    })))
})


@ns.route('/', strict_slashes=False)
class EmployeeList(Resource):
    @ns.marshal_list_with(employee_model)
    def get(self):
        """List all employees"""
        return Employee.query.all()

    @ns.expect(employee_model)
    @ns.marshal_with(employee_model, code=201)
    def post(self):
        '''Create a new employee'''
        data = request.json
        new_employee = Employee(
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
        )

        # Add dependents
        for dep in data.get('dependents', []):
            new_dependent = Dependent(
                first_name=dep['first_name'],
                last_name=dep['last_name'],
                relationship=dep['relationship'],
                date_of_birth=datetime.strptime(dep['date_of_birth'], '%Y-%m-%d'),
                employee=new_employee
            )
            db.session.add(new_dependent)

        db.session.add(new_employee)
        db.session.commit()
        return new_employee, 201


@ns.route('/<int:id>', strict_slashes=False)
@ns.response(404, 'Employee not found')
@ns.param('id', 'The employee identifier')
class EmployeeResource(Resource):
    @ns.marshal_with(employee_model)
    def get(self, id):
        """Fetch an employee given its identifier"""
        employee = Employee.query.get_or_404(id)
        return employee

    @ns.response(204, 'Employee deleted')
    def delete(self, id):
        """Delete an employee given its identifier"""
        employee = Employee.query.get_or_404(id)
        # Delete all dependents first
        for dependent in employee.dependents:
            db.session.delete(dependent)

        db.session.delete(employee)
        db.session.commit()
        return '', 204


@ns.route('/<int:id>/benefits', strict_slashes=False)
@ns.response(404, 'Employee not found')
@ns.param('id', 'The employee identifier')
class EmployeeBenefits(Resource):
    def get(self, id):
        """Calculate the benefits cost for an employee"""
        employee = Employee.query.get_or_404(id)
        cost = calculate_benefits_cost(employee)
        return jsonify({'employee_id': id, 'benefits_cost': cost})
