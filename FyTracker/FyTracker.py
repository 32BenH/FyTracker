# FyTracker
# Takes in a .csv file of all bank transactions and automatically sorts them into groups and then displays a graph of the data
# Author: Ben Hayden

import csv
import msvcrt
import pickle
import calendar
import matplotlib.pyplot as plt
from datetime import date
import Records

# ------------------------------------------------------------------------------------------------------------------------
# loading a dat file
def loadFromFile(fileName):
	# creating the file name
	# by default the file is being saved in working the directory
	filePathName = './' + fileName

	# open the file
	with open(filePathName, 'rb') as fp:
		# deserialize the data and return it
		return pickle.load(fp)
# ------------------------------------------------------------------------------------------------------------------------
# globals
try:
	# try to load the checkbook from a file
	checkbook = loadFromFile('checkbook')
except:
	# if the checkbook can't be loaded in create one
	checkbook = Records.Checkbook()

try:
	# try to load the categories from a file
	categories = loadFromFile('categories')
except:
	# if the checkbook can't be loaded in create one
	categories = []
	
userInput = 0
curYear = 2019 #date.today().year
curMonth = 12 #date.today().month
# ------------------------------------------------------------------------------------------------------------------------
# saving to a dat file
def saveToFile(fileName, data):
	# creating the file name
	# by default the file is being saved in the working directory
	filePathName = './' + fileName

	# open the file
	with open(filePathName, 'wb') as fp:
		# serialize the data and save it in the file that was opened
		pickle.dump(data, fp)
# ------------------------------------------------------------------------------------------------------------------------
# edit categories
def editCategories():
	while True:
		# print out the edit category options
		print("1. View categories")
		print("2. Add category")
		print("3. Remove categories")
		print("4. Back")

		# get the user input
		userInput = input("Selection: ")
		print(" ")

		# if the user hits view categories and there are no categories
		if int(userInput) == 1 and len(categories) < 1:
			print("No categories")
			print(" ")
			continue
		# if the user hits view categories
		elif int(userInput) == 1:
			count = 1
			# loop through all the categories and print them out
			for category in categories:
				print(str(count) + ". " + category.capitalize())
				count += 1

			# print out back at the end of all the categories
			print(str(count) + ". Back")

			# checks to see if the user hits back
			while True:
				# get the input
				userInput = input("Selection: ")
				print(" ")

				if int(userInput) == count:
					break
		# if the user hits add category
		elif int(userInput) == 2:
			# prompt the user for a new category
			new = input("Enter new category: ")
			print(" ")

			# add the new category to the list
			categories.append(new.lower())

			# save the categories
			saveToFile("categories", categories)
		#if the user hits remove categories
		elif int(userInput) == 3:
			count = 1
			# loop through all the categories and print them
			for category in categories:
				print(str(count) + ". " + category.capitalize())
				count += 1

			# show the extra actions
			print(str(count) + ". Remove all")
			print(str(count + 1) + ". Back")
			print("Choose a category to remove")

			# get the user input
			userInput = input("Selection: ")
			print(" ")

			# if the user hits remove all
			if int(userInput) == count:
				# clear the categories
				categories.clear()

				# save the categories
				saveToFile("categories", categories)
			# if the user hits back
			elif int(userInput) == count + 1:
				continue
			# if the user clicks on any of the categories
			elif int(userInput) < count:
				# delete the specified category
				del categories[int(userInput) - 1]

				# save the categories
				saveToFile("categories", categories)
			# wrong input
			else:
				print("Wrong input")
				continue
			pass
		# if the user hits exit
		elif int(userInput) == 4:
			break
		# wrong input
		else:
			print("Wrong input")
# ------------------------------------------------------------------------------------------------------------------------
# categorize the transaction
def categorize(row):
	# print out the transaction details
	print("Date: " + row[2])
	print("Company: " + row[4].strip())
	print("Amount: $" + row[6])
	print("Select your category")

	count = 1
	# loop through the categories and print them out
	for category in categories:
		print(str(count) + ". " + category.capitalize())
		count += 1

	# show an option to add a new category
	print(str(count) + ". Add new")

	# get the user input
	userInput = input("Selection: ")
	print(" ")
	
	# if the user hits a category
	if int(userInput) <= len(categories):
		# return the selected category
		return categories[int(userInput) - 1]
	# if the user hits add new
	else:
		# get the new category name
		new = input("Enter new category: ")
		print(" ")

		# add the new category to the list
		categories.append(new.lower())

		# save the categories77
		saveToFile("categories", categories)
		return new.lower()
# ------------------------------------------------------------------------------------------------------------------------
# input data
def inputData():
	while True:
		try:
			# get the .csv file path
			path = input("Paste the .csv file path: ")
			print(" ")

			# open the .csv
			with open(path) as csvfile:
				# read in all the lines of the .csv
				readCSV = csv.reader(csvfile, delimiter=',')
		
				# loop through all the lines of the .csv
				for row in readCSV:
					# get the current year
					rowYear = row[2].split('/')[2]
					# get the current month
					rowMonth = row[2].split('/')[0]

					# check to see if the year is already in the checkbook
					if not any(year for year in checkbook.years if year.year == rowYear):
						checkbook.addYear(rowYear)

					# find the index of the current year
					yearIndex = getYearIndex(rowYear)

					# check to see if the year is already in that specific year
					if not any(month for month in checkbook.years[yearIndex].months if month.month == rowMonth):
						checkbook.years[yearIndex].addMonth(rowMonth)

					# find the index of the month
					monthIndex = getMonthIndex(rowYear, rowMonth)

					# check to see if the transaction is already in that month
					if any(trans for trans in checkbook.years[yearIndex].months[monthIndex].transactions if trans.date == row[2].split('/')[1] and trans.company == row[4].strip() and trans.amount == float(row[6])):
						# print out a error message when the transaction is a duplicate
						print("!!Transaction already in checkbook!!")
						# print the duplicate transaction
						print(row[2].split('/')[1] + " " + row[4].strip() + " $" + row[6])
						# ask the user what they want to do with the duplicate transaction
						userIn = input("Do you want to keep this transaction(y or n): ")
						print(" ")

						# if the user wants to keep it
						if userIn == 'y':
							# get the category
							category = categorize(row)
							# add the transaction
							checkbook.years[yearIndex].months[monthIndex].addTransaction(row[2].split('/')[1], row[4].strip(), float(row[6]), category)
					else:
						# get the category
						category = categorize(row)
						# add the transaction
						checkbook.years[yearIndex].months[monthIndex].addTransaction(row[2].split('/')[1], row[4].strip(), float(row[6]), category)

				# sort transaction by date
				checkbook.years[yearIndex].months[monthIndex].transactions.sort(key=lambda x: x.date, reverse=False)
			break
		except:
			print("Not a valid path")
			continue
# ------------------------------------------------------------------------------------------------------------------------
def getYearIndex(yearInput):
	# find the index of the current year
	for count, year in enumerate(checkbook.years):
		if year.year == str(yearInput):
			return count
# ------------------------------------------------------------------------------------------------------------------------
def getMonthIndex(yearInput, monthInput):
	# find the index of the month
	yearIndex = getYearIndex(yearInput)
	for count, month in enumerate(checkbook.years[yearIndex].months):
		if month.month == str(monthInput):
			return count
# ------------------------------------------------------------------------------------------------------------------------
def displayMonth():
	# find the index of the current year
	try:
		yearIndex = getYearIndex(curYear)
		monthIndex = getMonthIndex(curYear, curMonth)
	except:
		print("No data for that month")
		return

	graphIncomeAmounts = [0] * len(categories)
	graphExpenseAmounts = [0] * len(categories)

	for count, transaction in enumerate(checkbook.years[yearIndex].months[monthIndex].transactions):
		index = categories.index(transaction.category)
		if transaction.category == "paid for":
			continue
		elif transaction.amount < 0:
			graphExpenseAmounts[index] += abs(transaction.amount)
		else:
			graphIncomeAmounts[index] += transaction.amount
	
	plt.rcParams['toolbar'] = 'None'
	fig, (ax1, ax2) = plt.subplots(1, 2)
	ax1.set_title("Expenses")
	ax2.set_title("Incomes")
	ax1.pie(graphExpenseAmounts, labels=categories, autopct=lambda p: '{:.0f}'.format(p * sum(graphExpenseAmounts) / 100) if p > 0 else '')
	ax2.pie(graphIncomeAmounts, labels=categories, autopct=lambda p: '{:.0f}'.format(p * sum(graphIncomeAmounts) / 100) if p > 0 else '')
	plt.show()
# ------------------------------------------------------------------------------------------------------------------------
def displayYear():
	# find the index of the current year
	try:
		yearIndex = getYearIndex(curYear)
		monthIndex = getMonthIndex(curYear, curMonth)
	except:
		print("No data for that month")
		return

	graphIncomeAmounts = [0] * len(categories)
	graphExpenseAmounts = [0] * len(categories)

	for year in checkbook.years:
		for month in checkbook.years[yearIndex].months:
			for transaction in checkbook.years[yearIndex].months[monthIndex].transactions:
				index = categories.index(transaction.category)
				if transaction.category == "paid for":
					continue
				elif transaction.amount < 0:
					graphExpenseAmounts[index] += abs(transaction.amount)
				else:
					graphIncomeAmounts[index] += transaction.amount

	plt.rcParams['toolbar'] = 'None'
	fig, (ax1, ax2) = plt.subplots(1, 2)
	ax1.set_title("Expenses")
	ax2.set_title("Incomes")
	ax1.pie(graphExpenseAmounts, labels=categories, autopct=lambda p: '{:.0f}'.format(p * sum(graphExpenseAmounts) / 100) if p > 0 else '')
	ax2.pie(graphIncomeAmounts, labels=categories, autopct=lambda p: '{:.0f}'.format(p * sum(graphIncomeAmounts) / 100) if p > 0 else '')
	plt.show()
# ------------------------------------------------------------------------------------------------------------------------
# edits the current selected date
def editDate():
	global curYear
	global curMonth

	# display instructions
	print("Select a new year")

	count = 1
	# loop through all the years and print them out
	for year in checkbook.years:
		print(str(count) + ". " + year.year)
		count += 1

	# print out back at the end of all the years
	print(str(count) + ". Back")

	# get the user input
	userInput = input("Selection: ")
	print(" ")

	if int(userInput) != count:
		# assign the new current year
		curYear = checkbook.years[int(userInput) - 1].year
	else:
		return
		
	# find the index of the current year
	yearIndex = getYearIndex(curYear)

	# display instructions
	print("Select a new month")

	count = 1
	# loop through all the months and print them out
	for month in checkbook.years[yearIndex].months:
		print(str(count) + ". " + month.month)
		count += 1

	# print out back at the end of all the months
	print(str(count) + ". Back")

	# get the user input
	userInput = input("Selection: ")
	print(" ")

	if int(userInput) != count:
		# assign the new current month
		curMonth = checkbook.years[yearIndex].months[int(userInput) - 1].month
# ------------------------------------------------------------------------------------------------------------------------
# main
while userInput != 5:
	# show the current year and month
	print("Current date: " + calendar.month_name[int(curMonth)] + " " + str(curYear))

	# display the menu options
	print("1. Input new data")
	print("2. Display current month graph")
	print("3. Display current year graph")
	print("4. Edit categories")
	print("5. Edit current date")
	print("6. Quit")

	# get the user input
	userInput = input("Selection: ")
	print(" ")

	# input new data
	if int(userInput) == 1:
		# input the data
		inputData()

		# save the data to a file
		saveToFile("checkbook", checkbook)
	# display the month graph
	elif int(userInput) == 2:
		displayMonth()
	# display the year graph
	elif int(userInput) == 3:
		displayYear()
	# edit category option
	elif int(userInput) == 4:
		# edit the categories
		editCategories()
		pass
	# edit the current month and year
	elif int(userInput) == 5:
		# edit the date
		editDate()
	# exit
	elif int(userInput) == 6:
		break
	# wrong input
	else:
		print("Wrong input")