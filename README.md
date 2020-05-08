# Enterprise-Resource-Planner-Blockchain
Highly abstracted blockchain management system for enterprise resource planning. Developed to allow for financial, human resources, client, supply, project, and schedule information to be managed using blockchains. Includes several features to add, remove, and query information on the chain. Uses a basic implementation of a web-based API, but most implementation is currently hard coded in place of a proper GUI.

# Features
* Expense tracking and management
* Revenue stream tracking and management
* Employee payroll, hiring, and overtime management
* Human Resources and complaint filing
* Client management information
* Project status and budgeting management
* Business supply monitoring system
* Employee scheduling service

# Information for use
To use this software, a google form exists at https://forms.gle/2rq5oFxLcyPPZo6EA. 
This form will allow you to enter information necessary to perform commands. Once entered, wait around 2-10 minutes for Google to process and update the database, and then run the main.py script. Unfortunately, this method does not yet work for every command case as of yet. In order to execute it manually, the below commands are available to be typed at the bottom of main.py to execute. If you would like to see the individual blocks of the chain, you can naviagte through the folders in the project file. Index 1 represents that chain's genesis node, and the following are all subsequent nodes.

#### FINANCIAL INFORMATION TRACKER:
expense_chain.add_expense(amount, employee_id, reason)
expense_chain.add_misc_expense(amount, employee_id, reason)
expense_chain.add_salary(amount, employee_id, reason)
expense_chain.add_loss(amount, employee_id, reason)
revenue_chain.add_revenue(amount, employee_id, reason)
revenue_chain.remove_revenue(amount, employee_id, reason)
print(expense_chain.expense_calc())
print(revenue_chain.calculate_revenue())
print(revenue_chain)
print(expense_chain)

#### HR INFORMATION TRACKER:
employee_chain.add_employee(name, salary, department, supervisor_id, employee_id)
employee_chain.remove_employee(name, salary, department, supervisor_id, employee_id)
print(employee_chain.get_employee_count())
print(employee_chain)
complaint_chain.add_complaint(description, employee1_id, employee2_id)
complaint_chain.retract_complaint(description, employee1_id, employee2_id)
complaint_chain.get_complaint(employee1_id)
print(complaint_chain)

#### STANDARDIZING CLIENT INFORMATION:
client_chain.add_client(name, bank_num, account_num, type, bal)
client_chain.remove_client(name, bank_num, account_num, type, bal)
client_chain.calculate_revenue(name)
client_chain.get_client(name)
print(client_chain)

#### SUPPLY MANAGEMENT INFORMATION:
supply_chain.add_supply(name, quantity)
supply_chain.use_supply(name, quantity)
supply_chain.get_inventory(name)
print(supply_chain)

#### PROJECT/INVESTMENT MANAGEMENT INFORMATION:
project_chain.add_project(supervisor_id, workers, budget, name)
project_chain.remove_project(supervisor_id, workers, name)
print(project_chain.get_active_projects())
print(project_chain.get_project(name)
print(project_chain)

#### EMPLOYEE SCHEDULING INFORMATION:
schedule_chain.add_schedule(employee_id, day)
schedule_chain.remove_schedule(employee_id, day)
print(schedule_chain.get_schedule(day)
print(schedule_chain.get_employee(employee_id)
schedule_chain.swap_shifts(emp_id1, emp_id2, day1, day2)
print(schedule_chain)
