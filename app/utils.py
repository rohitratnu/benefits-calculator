def calculate_benefits_cost(employee):
    cost = 1000  # Base cost for employee
    if employee.first_name.startswith('A'):
        cost *= 0.9  # 10% discount

    for dependent in employee.dependents:
        dependent_cost = 500
        if dependent.first_name.startswith('A'):
            dependent_cost *= 0.9  # 10% discount
        cost += dependent_cost

    return cost
