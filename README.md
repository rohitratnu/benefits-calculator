# Benefits API

This is a Flask-based API for calculating employee benefits. The API allows you to manage employees and their dependents, and calculate the benefits cost based on specific business logic.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/flask_project.git
    cd benefits-calculator
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. Start the Flask application:
    ```sh
    python run.py
    ```

2. The API will be available at `http://127.0.0.1:5000/`

## API Endpoints
- swagger page for the api can be seen at `http://127.0.0.1:5000/api`

### Employees

- **GET /api/employees**: List all employees.
- **POST /api/employees**: Create a new employee.
    - Request body:
        ```json
          {
              "first_name": "Rohit",
              "last_name": "Rohit",
              "salary": 52000,
              "date_of_birth": "1990-01-01",
              "dependents": [
              {
                  "id": 1,
                  "first_name": "Wife fname",
                  "last_name": "Wife lname",
                  "relationship": "Spouse",
                  "date_of_birth": "1992-02-02"
              }
          ]
      }
        ```

- **GET /api/employees/{id}**: Fetch an employee by ID.
- **GET /api/employees/{id}/benefits**: Fetch an employee benefits by ID.
- **DELETE /api/employees/{id}**: Delete an employee by ID.
    
        ```

## Business Logic

The benefits cost is calculated based on the following rules:
- Base cost for an employee is $1000.
- Employees with a first name starting with 'A' get a 10% discount.
- Each dependent adds $500 to the cost.
- Dependents with a first name starting with 'A' get a 10% discount.

## Testing

To run the tests, use the following command:
```sh
python -m unittest discover tests
```
