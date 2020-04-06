# Class for transactions
class Transaction:
	def __init__(self, date, company, amount, category):
		self.date = date
		self.company = company
		self.amount = amount
		self.category = category

# class for months
class Month:
	def __init__(self, month):
		self.month = month
		self.transactions = []

	def addTransaction(self, date, company, amount, category):
		self.transactions.append(Transaction(date, company, amount, category))

# class for years
class Year:
	def __init__(self, year):
		self.year = year
		self.months = []

	def addMonth(self, month):
		self.months.append(Month(month))

# class for checkbooks
class Checkbook:
	def __init__(self):
		self.years = []

	def addYear(self, year):
		self.years.append(Year(year))