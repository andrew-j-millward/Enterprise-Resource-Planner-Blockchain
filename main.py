############################################################
# COVID-19 Reminder Bot - main.py
############################################################
#
# Author: Andrew Joseph Millward
#
############################################################
# Imports
############################################################

import os, hashlib, time, calendar, requests, re
from bs4 import BeautifulSoup

############################################################
# Base Data Types
############################################################

class Expense():
	def __init__(self, amount, employee_id, reason, tag, master_Chain):
		self.employee_id = employee_id
		self.amount = amount
		self.reason = reason
		self.time = time.time()
		self.tag = tag
		self.expense_Chain = ExpenseChain()
	def __repr__(self):
		return str([self.amount,  self.employee_id, self.reason, self.time, self.tag])

class Revenue():
	def __init__(self, amount, employee_id, reason):
		self.amount = amount
		self.employee_id = employee_id
		self.reason = reason
		self.time = time.time()
	def __repr__(self):
		return str([self.amount,  self.employee_id, self.reason, self.time])

class Employee():
	def __init__(self, name, salary, department, supervisor, employee_id):
		self.name = name
		self.net_expenses = 0
		self.salary = salary
		self.overtime = 0
		self.department = department
		self.supervisor = supervisor
		self.id = employee_id
	def __repr__(self):
		return str([self.name,  self.net_expenses, self.salary, self.overtime, self.department, self.supervisor, self.id, time.time()])

class Complaint():
	def __init__(self, description, employee1_id, employee2_id, time, active = 1):
		self.description = description
		self.employee1_id = employee1_id
		self.employee2_id = employee2_id
		self.time = time
		self.active = active
	def __repr__(self):
		return str([self.description,  self.employee1_id, self.employee2_id, self.time, self.active])

class Client():
	def __init__(self, name, bank_num, account_num, type_list, bal):
		self.name = name
		self.bank_num = bank_num
		self.account_num = account_num
		self.type_list = type_list
		self.bal = bal
		self.time = time.time()
	def __repr__(self):
		return str([self.name,  self.bank_num, self.account_num, self.type_list, self.bal, self.time])

class Supply():
	def __init__(self, name, quantity):
		self.name = name
		self.quantity = quantity
	def __repr__(self):
		return str([self.name, self.quantity, time.time()])

class Project():
	def __init__(self, supervisor_id, workers, budget, name):
		self.supervisor_id = supervisor_id
		self.workers = workers
		self.budget = budget
		self.name = name
	def __repr__(self):
		return str([self.supervisor_id, self.workers, self.budget, self.name, time.time()])

class Schedule():
	def __init__(self, employee_id, day, cancelled = 0):
		self.employee_id = employee_id
		self.day = day
		self.cancelled = cancelled
	def __repr__(self):
		return str([self.employee_id, self.day, self.cancelled, time.time()])

############################################################
# Blockchain Classes
############################################################

class MasterChain:
	def __init__(self):
		self.current_transactions = []
		self.chain = refresh_chain("master")
		self.index = len(self.chain)+1

	def __repr__(self):
		result = """"""
		for i in range(len(self.chain)):
			result += "{\n\t'index': "+str(self.chain[i]['index'])+"\n\t'timestamp': "+str(self.chain[i]['timestamp'])+"\n\t'transactions': "+str(self.chain[i]['transactions'])+"\n\t'proof': "+str(self.chain[i]['proof'])+"\n\t'previous_hash': "+str(self.chain[i]['previous_hash'])+"\n\t'data': "+str(self.chain[i]['data'])+"\n}\n"
		return result

	@staticmethod
	def hash(data):
		#print(str(calendar.timegm(time.gmtime())))
		return hashlib.sha256(str(data).encode('utf-8')).hexdigest()

	@staticmethod
	def valid_proof(last_proof, proof, last_hash):
		guess = f'{last_proof}{proof}{last_hash}'.encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:4] == "0000"

	def proof_of_work(self):
		last_proof = self.chain[-1]['proof']
		last_hash = self.hash(self.chain[-1]['data'])

		proof = 0
		while self.valid_proof(last_proof, proof, last_hash) is False:
			proof += 1

		return proof

	def register_node(self, data):

		proof = self.proof_of_work()
		previous_hash = self.hash(self.chain[-1]['data'])

		block = {
			'index': len(self.chain)+1,
			'timestamp': time.time(),
			'transactions': self.current_transactions,
			'proof': proof,
			'previous_hash': previous_hash or self.hash(self.chain[-1]),
			"data": data
		}

		self.current_transactions = []
		new_file = open("master/master"+str(self.index)+".txt", "w")
		new_file.write("{\n\t'index': "+str(block['index'])+"\n\t'timestamp': "+str(block['timestamp'])+"\n\t'transactions': "+str(block['transactions'])+"\n\t'proof': "+str(block['proof'])+"\n\t'previous_hash': "+str(block['previous_hash'])+"\n\t'data': "+str(block['data'])+"\n}\n".replace("'", '"'))
		self.index += 1
		self.chain.append(block)
		new_file.close()
		self.chain = refresh_chain("master")
		return block

class ExpenseChain:
	def __init__(self):
		self.current_transactions = []
		self.chain = refresh_chain("expenses")
		self.index = len(self.chain)+1

	def __repr__(self):
		result = """"""
		for i in range(len(self.chain)):
			result += "{\n\t'index': "+str(self.chain[i]['index'])+"\n\t'timestamp': "+str(self.chain[i]['timestamp'])+"\n\t'transactions': "+str(self.chain[i]['transactions'])+"\n\t'proof': "+str(self.chain[i]['proof'])+"\n\t'previous_hash': "+str(self.chain[i]['previous_hash'])+"\n\t'data': "+str(self.chain[i]['data'])+"\n}\n"
		return result

	@staticmethod
	def hash(data):
		#print(str(calendar.timegm(time.gmtime())))
		return hashlib.sha256(str(data).encode('utf-8')).hexdigest()

	@staticmethod
	def valid_proof(last_proof, proof, last_hash):
		guess = f'{last_proof}{proof}{last_hash}'.encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:4] == "0000"

	def proof_of_work(self):
		last_proof = self.chain[-1]['proof']
		last_hash = self.hash(self.chain[-1]['data'])

		proof = 0
		while self.valid_proof(last_proof, proof, last_hash) is False:
			proof += 1

		return proof

	def register_node(self, data):

		proof = self.proof_of_work()
		previous_hash = self.hash(self.chain[-1]['data'])

		block = {
			'index': len(self.chain)+1,
			'timestamp': time.time(),
			'transactions': self.current_transactions,
			'proof': proof,
			'previous_hash': previous_hash or self.hash(self.chain[-1]),
			"data": data
		}

		self.current_transactions = []
		new_file = open("expenses/expenses"+str(self.index)+".txt", "w")
		new_file.write("{\n\t'index': "+str(block['index'])+"\n\t'timestamp': "+str(block['timestamp'])+"\n\t'transactions': "+str(block['transactions'])+"\n\t'proof': "+str(block['proof'])+"\n\t'previous_hash': "+str(block['previous_hash'])+"\n\t'data': "+str(block['data'])+"\n}\n".replace("'", '"'))
		self.index += 1
		self.chain.append(block)
		new_file.close()
		self.chain = refresh_chain("expenses")
		return block

	def add_expense(self, amount, employee_id, reason, tag=0):
		cur_time = time.time()
		expense_report = Expense(amount, employee_id, reason, tag, cur_time)
		master_chain.register_node(expense_report)
		self.register_node(expense_report)
		return( 0 )

	def add_misc_expense(self, amount, employee_id, reason):
		self.add_expense(amount, employee_id, reason, 0)

	def add_salary(self, amount, employee_id, reason="Payroll"):
		self.add_expense(amount, employee_id, reason, 1)

	def add_loss(self, amount, employee_id, reason):
		self.add_expense(amount, employee_id, reason, 2)

	def expense_calc(self):
		rev_chain = revenue_chain.chain
		exp_chain = expense_chain.chain
		net_expense = 0
		sources = {}
		for i in exp_chain:
			if i['index'] != '1':
				item = i['data'].strip('][').split(', ')
				net_expense += float(item[0])
				sources[item[2]] = float(item[0])
		for i in rev_chain:
			if i['index'] != '1':
				item = i['data'].strip('][').split(', ')
				if item[2] in sources and sources[item[2]] == float(item[0]):
					net_expense -= float(item[0])
		return net_expense

class RevenueChain:
	def __init__(self):
		self.current_transactions = []
		self.chain = refresh_chain("revenue")
		self.index = len(self.chain)+1

	def __repr__(self):
		result = """"""
		for i in range(len(self.chain)):
			result += "{\n\t'index': "+str(self.chain[i]['index'])+"\n\t'timestamp': "+str(self.chain[i]['timestamp'])+"\n\t'transactions': "+str(self.chain[i]['transactions'])+"\n\t'proof': "+str(self.chain[i]['proof'])+"\n\t'previous_hash': "+str(self.chain[i]['previous_hash'])+"\n\t'data': "+str(self.chain[i]['data'])+"\n}\n"
		return result

	@staticmethod
	def hash(data):
		#print(str(calendar.timegm(time.gmtime())))
		return hashlib.sha256(str(data).encode('utf-8')).hexdigest()

	@staticmethod
	def valid_proof(last_proof, proof, last_hash):
		guess = f'{last_proof}{proof}{last_hash}'.encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:4] == "0000"

	def proof_of_work(self):
		last_proof = self.chain[-1]['proof']
		last_hash = self.hash(self.chain[-1]['data'])

		proof = 0
		while self.valid_proof(last_proof, proof, last_hash) is False:
			proof += 1

		return proof

	def register_node(self, data):

		proof = self.proof_of_work()
		previous_hash = self.hash(self.chain[-1]['data'])

		block = {
			'index': len(self.chain)+1,
			'timestamp': time.time(),
			'transactions': self.current_transactions,
			'proof': proof,
			'previous_hash': previous_hash or self.hash(self.chain[-1]),
			"data": data
		}

		self.current_transactions = []
		new_file = open("revenue/revenue"+str(self.index)+".txt", "w")
		new_file.write("{\n\t'index': "+str(block['index'])+"\n\t'timestamp': "+str(block['timestamp'])+"\n\t'transactions': "+str(block['transactions'])+"\n\t'proof': "+str(block['proof'])+"\n\t'previous_hash': "+str(block['previous_hash'])+"\n\t'data': "+str(block['data'])+"\n}\n".replace("'", '"'))
		self.index += 1
		self.chain.append(block)
		new_file.close()
		self.chain = refresh_chain("revenue")
		return block

	def add_revenue(self, amount, employee_id, reason):
		revenue_report = Revenue(amount, employee_id, reason)
		master_chain.register_node(revenue_report)
		self.register_node(revenue_report)
		return( 0 )

	def remove_revenue(self, amount, employee_id, reason, tag = 0):
		revenue_report = Expense(amount, employee_id, reason, tag, time.time())
		expense_chain.register_node(revenue_report)
		master_chain.register_node(expense_chain)
		return 0

	def revenue_calc(self):
		rev_chain = revenue_chain.chain
		exp_chain = expense_chain.chain
		net_revenue = 0
		sources = {}
		for i in rev_chain:
			if i['index'] != '1':
				item = i['data'].strip('][').split(', ')
				net_revenue += float(item[0])
				sources[item[2]] = float(item[0])
		for i in exp_chain:
			if i['index'] != '1':
				item = i['data'].strip('][').split(', ')
				if item[2] in sources and sources[item[2]] == float(item[0]):
					net_revenue -= float(item[0])
		return net_revenue

class EmployeeChain:
	def __init__(self):
		self.current_transactions = []
		self.chain = refresh_chain("employees")
		self.index = len(self.chain)+1

	def __repr__(self):
		result = """"""
		for i in range(len(self.chain)):
			result += "{\n\t'index': "+str(self.chain[i]['index'])+"\n\t'timestamp': "+str(self.chain[i]['timestamp'])+"\n\t'transactions': "+str(self.chain[i]['transactions'])+"\n\t'proof': "+str(self.chain[i]['proof'])+"\n\t'previous_hash': "+str(self.chain[i]['previous_hash'])+"\n\t'data': "+str(self.chain[i]['data'])+"\n}\n"
		return result

	@staticmethod
	def hash(data):
		#print(str(calendar.timegm(time.gmtime())))
		return hashlib.sha256(str(data).encode('utf-8')).hexdigest()

	@staticmethod
	def valid_proof(last_proof, proof, last_hash):
		guess = f'{last_proof}{proof}{last_hash}'.encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:4] == "0000"

	def proof_of_work(self):
		last_proof = self.chain[-1]['proof']
		last_hash = self.hash(self.chain[-1]['data'])

		proof = 0
		while self.valid_proof(last_proof, proof, last_hash) is False:
			proof += 1

		return proof

	def register_node(self, data):

		proof = self.proof_of_work()
		previous_hash = self.hash(self.chain[-1]['data'])

		block = {
			'index': len(self.chain)+1,
			'timestamp': time.time(),
			'transactions': self.current_transactions,
			'proof': proof,
			'previous_hash': previous_hash or self.hash(self.chain[-1]),
			"data": data
		}

		self.current_transactions = []
		new_file = open("employees/employees"+str(self.index)+".txt", "w")
		new_file.write("{\n\t'index': "+str(block['index'])+"\n\t'timestamp': "+str(block['timestamp'])+"\n\t'transactions': "+str(block['transactions'])+"\n\t'proof': "+str(block['proof'])+"\n\t'previous_hash': "+str(block['previous_hash'])+"\n\t'data': "+str(block['data'])+"\n}\n".replace("'", '"'))
		self.index += 1
		self.chain.append(block)
		new_file.close()
		self.chain = refresh_chain("employees")
		return block

	def add_employee(self, name, salary, department, supervisor, employee_id):
		new_employee = Employee(name, salary, department, supervisor, employee_id)
		master_chain.register_node(new_employee)
		self.register_node(new_employee)
		expense_chain.register_node(salary, employee_id, "Payroll", 2)
		return( 0 )

	def remove_employee(self, name, salary, department, supervisor, employee_id):
		fired_employee = Employee(name, salary, department, supervisor, 0)
		time1 = time.time()
		salary = 0
		for i in self.chain:
			if i['index'] != '1':
				item = i['data'].strip('][').split(', ')
				if item[6] == employee_id:
					time1 = item[7]
					salary = float(item[2])
		severance = (time.time()-time1)*salary/31536000

		employee_chain.register_node(fired_employee)
		master_chain.register_node(fired_employee)
		revenue_chain.add_revenue(salary, employee_id, "Fired")
		return severance

	def get_employee_count(self):
		emp_chain = employee_chain.chain
		employees = []
		for i in emp_chain:
			if i['index'] != '1':
				item = i['data'].strip('][').split(', ')
				if item[0] not in employees and item[6] != '0':
					employees.append(item[0])
				elif item[6] == '0' and item[0] in employees:
					employees.remove(item[0])
		return employees

class ComplaintChain:
	def __init__(self):
		self.current_transactions = []
		self.chain = refresh_chain("complaints")
		self.index = len(self.chain)+1

	def __repr__(self):
		result = """"""
		for i in range(len(self.chain)):
			result += "{\n\t'index': "+str(self.chain[i]['index'])+"\n\t'timestamp': "+str(self.chain[i]['timestamp'])+"\n\t'transactions': "+str(self.chain[i]['transactions'])+"\n\t'proof': "+str(self.chain[i]['proof'])+"\n\t'previous_hash': "+str(self.chain[i]['previous_hash'])+"\n\t'data': "+str(self.chain[i]['data'])+"\n}\n"
		return result

	@staticmethod
	def hash(data):
		#print(str(calendar.timegm(time.gmtime())))
		return hashlib.sha256(str(data).encode('utf-8')).hexdigest()

	@staticmethod
	def valid_proof(last_proof, proof, last_hash):
		guess = f'{last_proof}{proof}{last_hash}'.encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:4] == "0000"

	def proof_of_work(self):
		last_proof = self.chain[-1]['proof']
		last_hash = self.hash(self.chain[-1]['data'])

		proof = 0
		while self.valid_proof(last_proof, proof, last_hash) is False:
			proof += 1

		return proof

	def register_node(self, data):

		proof = self.proof_of_work()
		previous_hash = self.hash(self.chain[-1]['data'])

		block = {
			'index': len(self.chain)+1,
			'timestamp': time.time(),
			'transactions': self.current_transactions,
			'proof': proof,
			'previous_hash': previous_hash or self.hash(self.chain[-1]),
			"data": data
		}

		self.current_transactions = []
		new_file = open("complaints/complaints"+str(self.index)+".txt", "w")
		new_file.write("{\n\t'index': "+str(block['index'])+"\n\t'timestamp': "+str(block['timestamp'])+"\n\t'transactions': "+str(block['transactions'])+"\n\t'proof': "+str(block['proof'])+"\n\t'previous_hash': "+str(block['previous_hash'])+"\n\t'data': "+str(block['data'])+"\n}\n".replace("'", '"'))
		self.index += 1
		self.chain.append(block)
		new_file.close()
		self.chain = refresh_chain("complaints")
		return block

	def add_complaint(self, description, employee1_id, employee2_id):
		new_complaint = Complaint(description, employee1_id, employee2_id, time.time())
		master_chain.register_node(new_complaint)
		self.register_node(new_complaint)
		return( 0 )

	def retract_complaint(self, description, employee1_id, employee2_id):
		retracted_complaint = Complaint(description, employee1_id, employee2_id, time.time(), 0)
		self.register_node(retracted_complaint)
		master_chain.register_node(retracted_complaint)

	def get_complaint(self, employee1_id):
		com_chain = complaint_chain.chain
		complaints = []
		for i in com_chain:
			if i['index'] != '1':
				item = i['data'].strip('][').split(', ')
				if item[0] not in complaints and item[4] != '0' and item[1] == str(employee1_id):
					complaints.append(item[0])
				elif item[4] == '0' and item[0] in complaints:
					complaints.remove(item[0])
		return complaints

class ClientChain:
	def __init__(self):
		self.current_transactions = []
		self.chain = refresh_chain("clients")
		self.index = len(self.chain)+1

	def __repr__(self):
		result = """"""
		for i in range(len(self.chain)):
			result += "{\n\t'index': "+str(self.chain[i]['index'])+"\n\t'timestamp': "+str(self.chain[i]['timestamp'])+"\n\t'transactions': "+str(self.chain[i]['transactions'])+"\n\t'proof': "+str(self.chain[i]['proof'])+"\n\t'previous_hash': "+str(self.chain[i]['previous_hash'])+"\n\t'data': "+str(self.chain[i]['data'])+"\n}\n"
		return result

	@staticmethod
	def hash(data):
		#print(str(calendar.timegm(time.gmtime())))
		return hashlib.sha256(str(data).encode('utf-8')).hexdigest()

	@staticmethod
	def valid_proof(last_proof, proof, last_hash):
		guess = f'{last_proof}{proof}{last_hash}'.encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:4] == "0000"

	def proof_of_work(self):
		last_proof = self.chain[-1]['proof']
		last_hash = self.hash(self.chain[-1]['data'])

		proof = 0
		while self.valid_proof(last_proof, proof, last_hash) is False:
			proof += 1

		return proof

	def register_node(self, data):

		proof = self.proof_of_work()
		previous_hash = self.hash(self.chain[-1]['data'])

		block = {
			'index': len(self.chain)+1,
			'timestamp': time.time(),
			'transactions': self.current_transactions,
			'proof': proof,
			'previous_hash': previous_hash or self.hash(self.chain[-1]),
			"data": data
		}

		self.current_transactions = []
		new_file = open("clients/clients"+str(self.index)+".txt", "w")
		new_file.write("{\n\t'index': "+str(block['index'])+"\n\t'timestamp': "+str(block['timestamp'])+"\n\t'transactions': "+str(block['transactions'])+"\n\t'proof': "+str(block['proof'])+"\n\t'previous_hash': "+str(block['previous_hash'])+"\n\t'data': "+str(block['data'])+"\n}\n".replace("'", '"'))
		self.index += 1
		self.chain.append(block)
		new_file.close()
		self.chain = refresh_chain("clients")
		return block

	def add_client(self, name, bank_num, account_num, type_list, bal):
		new_client = Client(name, bank_num, account_num, type_list, bal)
		master_chain.register_node(new_client)
		self.register_node(new_client)
		return( 0 )

	def remove_client(self, name, bank_num, account_num, type_list, bal):
		retracted_client = Client(name, bank_num, 0, type_list, bal)
		self.register_node(retracted_client)
		master_chain.register_node(retracted_client)
		return bal

	def calculate_revenue(self, name):
		cli_chain = client_chain.chain
		bal = 0
		for i in cli_chain:
			if i['index'] != '1':
				item = i['data'].strip('][').split(', ')
				if item[2] != '0' and item[0] == name:
					bal = item[4]
				if item[2] == '0' and item[0] == name:
					bal = 0
		revenue = float(bal)*0.07 # Assuming average 7% return on loans.
		return revenue

	def get_client(self, name):
		cli_chain = client_chain.chain
		client = []
		for i in cli_chain:
			if i['index'] != '1':
				item = i['data'].strip('][').split(', ')
				if item[2] != '0' and item[0] == name:
					client.append(item)
				if item[2] == '0' and item[0] == name:
					try:
						del[client[-1]]
					except: pass
		return client

class SupplyChain:
	def __init__(self):
		self.current_transactions = []
		self.chain = refresh_chain("supply")
		self.index = len(self.chain)+1

	def __repr__(self):
		result = """"""
		for i in range(len(self.chain)):
			result += "{\n\t'index': "+str(self.chain[i]['index'])+"\n\t'timestamp': "+str(self.chain[i]['timestamp'])+"\n\t'transactions': "+str(self.chain[i]['transactions'])+"\n\t'proof': "+str(self.chain[i]['proof'])+"\n\t'previous_hash': "+str(self.chain[i]['previous_hash'])+"\n\t'data': "+str(self.chain[i]['data'])+"\n}\n"
		return result

	@staticmethod
	def hash(data):
		#print(str(calendar.timegm(time.gmtime())))
		return hashlib.sha256(str(data).encode('utf-8')).hexdigest()

	@staticmethod
	def valid_proof(last_proof, proof, last_hash):
		guess = f'{last_proof}{proof}{last_hash}'.encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:4] == "0000"

	def proof_of_work(self):
		last_proof = self.chain[-1]['proof']
		last_hash = self.hash(self.chain[-1]['data'])

		proof = 0
		while self.valid_proof(last_proof, proof, last_hash) is False:
			proof += 1

		return proof

	def register_node(self, data):

		proof = self.proof_of_work()
		previous_hash = self.hash(self.chain[-1]['data'])

		block = {
			'index': len(self.chain)+1,
			'timestamp': time.time(),
			'transactions': self.current_transactions,
			'proof': proof,
			'previous_hash': previous_hash or self.hash(self.chain[-1]),
			"data": data
		}

		self.current_transactions = []
		new_file = open("supply/supply"+str(self.index)+".txt", "w")
		new_file.write("{\n\t'index': "+str(block['index'])+"\n\t'timestamp': "+str(block['timestamp'])+"\n\t'transactions': "+str(block['transactions'])+"\n\t'proof': "+str(block['proof'])+"\n\t'previous_hash': "+str(block['previous_hash'])+"\n\t'data': "+str(block['data'])+"\n}\n".replace("'", '"'))
		self.index += 1
		self.chain.append(block)
		new_file.close()
		self.chain = refresh_chain("supply")
		return block

	def add_supply(self, name, quantity):
		new_supply = Supply(name, quantity)
		master_chain.register_node(new_supply)
		self.register_node(new_supply)
		return( 0 )

	def use_supply(self, name, quantity):
		removed_supply = Supply(name, -quantity)
		self.register_node(removed_supply)
		master_chain.register_node(removed_supply)

	def get_inventory(self, name):
		sup_chain = supply_chain.chain
		quant = 0
		for i in sup_chain:
			if i['index'] != '1':
				item = i['data'].strip('][').split(', ')
				if item[0] == name:
					quant += float(item[1])
		return quant

class ProjectChain:
	def __init__(self):
		self.current_transactions = []
		self.chain = refresh_chain("projects")
		self.index = len(self.chain)+1

	def __repr__(self):
		result = """"""
		for i in range(len(self.chain)):
			result += "{\n\t'index': "+str(self.chain[i]['index'])+"\n\t'timestamp': "+str(self.chain[i]['timestamp'])+"\n\t'transactions': "+str(self.chain[i]['transactions'])+"\n\t'proof': "+str(self.chain[i]['proof'])+"\n\t'previous_hash': "+str(self.chain[i]['previous_hash'])+"\n\t'data': "+str(self.chain[i]['data'])+"\n}\n"
		return result

	@staticmethod
	def hash(data):
		#print(str(calendar.timegm(time.gmtime())))
		return hashlib.sha256(str(data).encode('utf-8')).hexdigest()

	@staticmethod
	def valid_proof(last_proof, proof, last_hash):
		guess = f'{last_proof}{proof}{last_hash}'.encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:4] == "0000"

	def proof_of_work(self):
		last_proof = self.chain[-1]['proof']
		last_hash = self.hash(self.chain[-1]['data'])

		proof = 0
		while self.valid_proof(last_proof, proof, last_hash) is False:
			proof += 1

		return proof

	def register_node(self, data):

		proof = self.proof_of_work()
		previous_hash = self.hash(self.chain[-1]['data'])

		block = {
			'index': len(self.chain)+1,
			'timestamp': time.time(),
			'transactions': self.current_transactions,
			'proof': proof,
			'previous_hash': previous_hash or self.hash(self.chain[-1]),
			"data": data
		}

		self.current_transactions = []
		new_file = open("projects/projects"+str(self.index)+".txt", "w")
		new_file.write("{\n\t'index': "+str(block['index'])+"\n\t'timestamp': "+str(block['timestamp'])+"\n\t'transactions': "+str(block['transactions'])+"\n\t'proof': "+str(block['proof'])+"\n\t'previous_hash': "+str(block['previous_hash'])+"\n\t'data': "+str(block['data'])+"\n}\n".replace("'", '"'))
		self.index += 1
		self.chain.append(block)
		new_file.close()
		self.chain = refresh_chain("projects")
		return block

	def add_project(self, supervisor_id, workers, budget, name):
		new_project = Project(supervisor_id, workers, budget, name)
		master_chain.register_node(new_project)
		self.register_node(new_project)
		return( 0 )

	def remove_project(self, supervisor_id, workers, name):
		removed_project = Project(supervisor_id, workers, 0, name)
		self.register_node(removed_project)
		master_chain.register_node(removed_project)

	def get_active_projects(self):
		pro_chain = project_chain.chain
		projects = []
		for i in pro_chain:
			if i['index'] != '1':
				item = i['data'].strip('][').split(', ')
				if item[2] != '0':
					projects.append(item[3])
				elif item[2] == '0' and item[3] in projects:
					projects.remove(item[3])
		return projects

	def get_project(self, name):
		pro_chain = project_chain.chain
		projects = []
		for i in pro_chain:
			if i['index'] != '1':
				item = i['data'].strip('][').split(', ')
				if item[2] != '0' and item[3] == name:
					projects = item
				elif item[2] == '0' and item[3] == name:
					projects = []
		return projects

class ScheduleChain:
	def __init__(self):
		self.current_transactions = []
		self.chain = refresh_chain("schedule")
		self.index = len(self.chain)+1

	def __repr__(self):
		result = """"""
		for i in range(len(self.chain)):
			result += "{\n\t'index': "+str(self.chain[i]['index'])+"\n\t'timestamp': "+str(self.chain[i]['timestamp'])+"\n\t'transactions': "+str(self.chain[i]['transactions'])+"\n\t'proof': "+str(self.chain[i]['proof'])+"\n\t'previous_hash': "+str(self.chain[i]['previous_hash'])+"\n\t'data': "+str(self.chain[i]['data'])+"\n}\n"
		return result

	@staticmethod
	def hash(data):
		#print(str(calendar.timegm(time.gmtime())))
		return hashlib.sha256(str(data).encode('utf-8')).hexdigest()

	@staticmethod
	def valid_proof(last_proof, proof, last_hash):
		guess = f'{last_proof}{proof}{last_hash}'.encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:4] == "0000"

	def proof_of_work(self):
		last_proof = self.chain[-1]['proof']
		last_hash = self.hash(self.chain[-1]['data'])

		proof = 0
		while self.valid_proof(last_proof, proof, last_hash) is False:
			proof += 1

		return proof

	def register_node(self, data):

		proof = self.proof_of_work()
		previous_hash = self.hash(self.chain[-1]['data'])

		block = {
			'index': len(self.chain)+1,
			'timestamp': time.time(),
			'transactions': self.current_transactions,
			'proof': proof,
			'previous_hash': previous_hash or self.hash(self.chain[-1]),
			"data": data
		}

		self.current_transactions = []
		new_file = open("schedule/schedule"+str(self.index)+".txt", "w")
		new_file.write("{\n\t'index': "+str(block['index'])+"\n\t'timestamp': "+str(block['timestamp'])+"\n\t'transactions': "+str(block['transactions'])+"\n\t'proof': "+str(block['proof'])+"\n\t'previous_hash': "+str(block['previous_hash'])+"\n\t'data': "+str(block['data'])+"\n}\n".replace("'", '"'))
		self.index += 1
		self.chain.append(block)
		new_file.close()
		self.chain = refresh_chain("schedule")
		return block

	def add_schedule(self, employee_id, day):
		new_schedule = Schedule(employee_id, day)
		master_chain.register_node(new_schedule)
		self.register_node(new_schedule)
		return( 0 )

	def remove_schedule(self, employee_id, day):
		removed_schedule = Schedule(employee_id, day, 1)
		self.register_node(removed_schedule)
		master_chain.register_node(removed_schedule)

	def get_schedule(self, day):
		sch_chain = schedule_chain.chain
		schedule = []
		for i in sch_chain:
			if i['index'] != '1':
				item = i['data'].strip('][').split(', ')
				if item[2] != '1' and str(day) == item[1]:
					schedule.append(item[0])
				elif item[2] == '1' and item[0] in schedule and str(day) == item[1]:
					schedule.remove(item[0])
		return schedule

	def get_employee(self, emp_id):
		sch_chain = schedule_chain.chain
		schedule = []
		for i in sch_chain:
			if i['index'] != '1':
				item = i['data'].strip('][').split(', ')
				if item[2] != '1' and str(emp_id) == item[0]:
					schedule.append(item[1])
				elif item[2] == '1' and item[1] in schedule and str(emp_id) == item[0]:
					schedule.remove(item[1])
		return schedule

	def swap_shifts(self, emp_id1, emp_id2, day1, day2):
		pro_chain = project_chain.chain
		emp1_sch = self.get_employee(emp_id1)
		emp2_sch = self.get_employee(emp_id2)
		print(emp1_sch, emp2_sch)
		if str(day1) not in emp2_sch and str(day2) not in emp1_sch:
			print("hi")
			self.remove_schedule(emp_id1, day1)
			self.remove_schedule(emp_id2, day2)
			self.add_schedule(emp_id1, day2)
			self.add_schedule(emp_id2, day1)

############################################################
# Functions
############################################################

def refresh_chain(chain_folder):

	# Blocks should be organized alphabetically
	# Grab each file in the chain.
	files = []
	for i in os.walk(chain_folder):
		for file in i[2]:
			files.append(file)
	
	# Process the data in each file and update the blockchain
	chain = []
	for file in files:
		data = open(chain_folder+"/"+file, "r")
		data = data.readlines()
		del[data[-1]]
		del[data[0]]
		for j in range(len(data)):
			data[j] = data[j].strip()
			data[j] = data[j].split(":", 1)
			for k in range(len(data[j])):
				data[j][k] = data[j][k].strip().replace('"', "'").replace("'","")
		for i in data:
			block = {
				data[0][0]:data[0][1],
				data[1][0]:data[1][1],
				data[2][0]:data[2][1],
				data[3][0]:data[3][1],
				data[4][0]:data[4][1],
				data[5][0]:data[5][1]
			}
		chain.append(block)
	return chain
	
def get_commands():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQPRSEagSDOlfLLJiNmqmMb-0B2_ObDUWNf-00eXKnHQqFf2Nj2bkpvv9QJo5lS5u92MezF1pEGvh4T/pubhtml"
    request = requests.get(url)
    data = request.text
    soup = BeautifulSoup(data, "html.parser")
    table = soup.findAll("table")[0]
    rows = table.tbody.findAll("tr")
    command_list = []
    for i in range(len(rows)-2):
        row_contents = rows[i+2].findAll("td")
        command_list.append([row_contents[1].text, row_contents[2], row_contents[3].text, row_contents[4].text, row_contents[5].text, row_contents[6].text, row_contents[7], row_contents[8].text, row_contents[9].text, row_contents[10].text, row_contents[11].text, row_contents[12].text, row_contents[13].text])
    return command_list

def run_commands(command_list):
	command_num = open("LastCommand.txt", "a+")
	command_num.seek(0)
	command_line = command_num.readlines()
	cur_line = int(command_line[-1].strip())
	# Run Commands
	for i in range(len(command_list)-cur_line):
		try:
			if command_list[cur_line+i][0] == "Financial Information Tracker":
				data = command_list[cur_line+i][2].split()
				for j in range(len(data)):
					data[j] = re.sub('<[^<]+?>', '', data[j])
				if command_list[cur_line+i][1] == "Log Expense (amount, employee_id, reason)":
					expense_chain.add_expense(float(data[0]), int(data[1]), data[2])
				elif command_list[cur_line+i][1] == "Add Misc Expense (amount, employee_id, reason)":
					expense_chain.add_misc_expense(float(data[0]), int(data[1]), data[2])
				elif command_list[cur_line+i][1] == "Add Salary (amount, employee_id, reason)":
					expense_chain.add_salary(float(data[0]), int(data[1]), data[2])
				elif command_list[cur_line+i][1] == "Add Loss (amount, employee_id, reason)":
					expense_chain.add_loss(float(data[0]), int(data[1]), data[2])
				elif command_list[cur_line+i][1] == "Add Revenue (amount, employee_id, reason)":
					revenue_chain.add_revenue(float(data[0]), int(data[1]), data[2])
				elif command_list[cur_line+i][1] == "Remove Revenue (amount, employee_id, reason)":
					revenue_chain.remove_revenue(float(data[0]), int(data[1]), data[2])
				elif command_list[cur_line+i][1] == "Calculate Expenses ()":
					print(expense_chain.expense_calc())
				elif command_list[cur_line+i][1] == "Calculate Revenue ()":
					print(revenue_chain.calculate_revenue())
				elif command_list[cur_line+i][1] == "Print Revenue Chain ()":
					print(revenue_chain)
				elif command_list[cur_line+i][1] == "Print Expense Chain ()":
					print(expense_chain)

			elif command_list[cur_line+i][0] == "Human Resources Information":
				data = command_list[cur_line+i][4].split()
				if command_list[cur_line+i][3] == "Add Employee (name, salary, department, supervisor_id, employee_id)":
					employee_chain.add_employee(data[0], float(data[1]), data[2], int(data[3]), int(data[4]))
				elif command_list[cur_line+i][3] == "Remove Employee (name, salary, department, supervisor_id, employee_id)":
					employee_chain.remove_employee(data[0], float(data[1]), data[2], int(data[3]), int(data[4]))
				elif command_list[cur_line+i][3] == "Get Employee Count ()":
					print(employee_chain.get_employee_count())
				elif command_list[cur_line+i][3] == "Print Employee Chain ()":
					print(employee_chain)
				elif command_list[cur_line+i][3] == "Add Complaint (description, employee1_id, employee2_id)":
					complaint_chain.add_complaint(data[0], int(data[1]), int(data[2]))
				elif command_list[cur_line+i][3] == "Retract Complaint (description, employee1_id, employee2_id)":
					complaint_chain.retract_complaint(data[0], int(data[1]), int(data[2]))
				elif command_list[cur_line+i][3] == "Get Complaint (employee1_id)":
					complaint_chain.get_complaint(data[0])
				elif command_list[cur_line+i][3] == "Print Complaint Chain ()":
					print(complaint_chain)

			elif command_list[cur_line+i][0] == "Bank Client Information":
				data = command_list[cur_line+i][6].split()
				if command_list[cur_line+i][5] == "Add Client (name, bank_num, account_num, type, bal)":
					client_chain.add_client(data[0], int(data[1]), int(data[2]), data[3], float(data[4]))
				elif command_list[cur_line+i][5] == "Remove Client (name, bank_num, account_num, type, bal)":
					client_chain.remove_client(data[0], int(data[1]), int(data[2]), data[3], float(data[4]))
				elif command_list[cur_line+i][5] == "Calculate Revenue (name)":
					client_chain.calculate_revenue(data[0])
				elif command_list[cur_line+i][5] == "Get Client (name)":
					client_chain.get_client(data[0])
				elif command_list[cur_line+i][5] == "Print Client Chain ()":
					print(client_chain)

			elif command_list[cur_line+i][0] == "Supply Management Information":
				data = command_list[cur_line+i][8].split()
				if command_list[cur_line+i][7] == "Add Supply (name, quantity)":
					supply_chain.add_supply(data[0], int(data[1]))
				elif command_list[cur_line+i][7] == "Use Supply (name, quantity)":
					supply_chain.use_supply(data[0], int(data[1]))
				elif command_list[cur_line+i][7] == "Get Inventory (name)":
					supply_chain.get_inventory(data[0])
				elif command_list[cur_line+i][7] == "Print Supply Chain ()":
					print(supply_chain)

			elif command_list[cur_line+i][0] == "Project/Investment Management Information":
				data = command_list[cur_line+i][10].split()
				if command_list[cur_line+i][9] == "Add Project (supervisor_id, workers, budget, name)":
					project_chain.add_project(int(data[0]), int(data[1]), float(data[2]), data[3])
				elif command_list[cur_line+i][9] == "Remove Project (supervisor_id, workers, name)":
					project_chain.remove_project(int(data[0]), int(data[1]), data[2])
				elif command_list[cur_line+i][9] == "Get Active Projects ()":
					print(project_chain.get_active_projects())
				elif command_list[cur_line+i][9] == "Get Project (name)":
					print(project_chain.get_project(data[0]))
				elif command_list[cur_line+i][9] == "Print Project Chain ()":
					print(project_chain)

			elif command_list[cur_line+i][0] == "Scheduling Information":
				data = command_list[cur_line+i][12].split()
				if command_list[cur_line+i][11] == "Add Schedule (employee_id, day)":
					schedule_chain.add_schedule(int(data[0]), int(data[1]))
				elif command_list[cur_line+i][11] == "Remove Schedule (employee_id, day)":
					schedule_chain.remove_schedule(int(data[0]), int(data[1]))
				elif command_list[cur_line+i][11] == "Get Schedule (day)":
					print(schedule_chain.get_schedule(int(data[0])))
				elif command_list[cur_line+i][11] == "Get Employee (employee_id)":
					print(schedule_chain.get_employee(int(data[0])))
				elif command_list[cur_line+i][11] == "Swap Shifts (emp_id1, emp_id2, day1, day2)":
					schedule_chain.swap_shifts(int(data[0]), int(data[1]), int(data[2]), int(data[3]))
				elif command_list[cur_line+i][11] == "Print Scheduling Chain ()":
					print(schedule_chain)

			command_num.write(str(cur_line+i+1)+"\n")
			command_num.seek(0)
			command_line = command_num.readlines()
		except:
			print("Error encountered with parameter input... Ignoring command...")

if __name__ == "__main__":
	master_chain = MasterChain()
	expense_chain = ExpenseChain()
	revenue_chain = RevenueChain()
	employee_chain = EmployeeChain()
	complaint_chain = ComplaintChain()
	client_chain = ClientChain()
	supply_chain = SupplyChain()
	project_chain = ProjectChain()
	schedule_chain = ScheduleChain()

	##################################################################
	##               Retrieve Google Forms Commands                 ##
	##################################################################

	commands = get_commands()
	run_commands(commands)

	##################################################################
	##                 Add codes beyond this point                  ##
	##################################################################

	

	#schedule_chain.swap_shifts(2, 3, 42, 43)
	#client_chain.remove_client("Alvin Lame", 4236243, 457458458, "Savings", 1232)
	#print(revenue_chain)
	#print(schedule_chain.get_employee(3))
	#print(schedule_chain)