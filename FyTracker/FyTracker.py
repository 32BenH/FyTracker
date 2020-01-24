# FyTracker
# Takes in a .csv file of all bank transactions and automatically sorts them into groups and then displays a graph of the data
# Author: Ben Hayden

import csv
import msvcrt
import pickle
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
		print(" ")

		# get the user input
		userInput = msvcrt.getch()

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
			print(" ")

			# checks to see if the user hits back
			while True:
				# get the input
				userInput = msvcrt.getch()

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
			print(" ")

			# get the user input
			userInput = msvcrt.getch()

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
	print(" ")

	# get the user input
	userInput = msvcrt.getch()
	
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

		# save the categories
		saveToFile("categories", categories)
		return new
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
					curYear = row[2].split('/')[2]
					# get the current month
					curMonth = row[2].split('/')[0]

					# check to see if the year is already in the checkbook
					if not any(year for year in checkbook.years if year.year == curYear):
						checkbook.addYear(curYear)

					# find the index of the current year
					for count, year in enumerate(checkbook.years):
						if year.year == curYear:
							yearIndex = count

					# check to see if the year is already in that specific year
					if not any(month for month in checkbook.years[yearIndex].months if month.month == curMonth):
						checkbook.years[yearIndex].addMonth(curMonth)

					# find the index of the month
					for count, month in enumerate(checkbook.years[yearIndex].months):
						if month.month == curMonth:
							monthIndex = count

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
# main
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

while userInput != 5:
	# display the menu options
	print("1. Display a month")
	print("2. Display a year")
	print("3. Input new data")
	print("4. Edit categories")
	print("5. Quit")
	print(" ")

	# get the user input
	userInput = msvcrt.getch()

	# display the month graph
	if int(userInput) == 1:
		pass
	# display the year graph
	elif int(userInput) == 2:
		pass
	# input new data
	elif int(userInput) == 3:
		# input the data
		inputData()

		# save the data to a file
		saveToFile("checkbook", checkbook)
	# edit category option
	elif int(userInput) == 4:
		# edit the categories
		editCategories()
		pass
	# exit
	elif int(userInput) == 5:
		break
	# wrong input
	else:
		print("Wrong input")