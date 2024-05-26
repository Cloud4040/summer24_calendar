import json
import csv
from datetime import datetime, timedelta

#gets the date for an item in the calendar
def get_date(prompt):
    while True:
        try:
            return datetime.strptime(input(prompt), '%Y-%m-%d')
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

#gets the time for an item in the calendar
def get_time(prompt):
    while True:
        try:
            return datetime.strptime(input(prompt), '%H:%M').time()
        except ValueError:
            print("Invalid time format. Please use HH:MM.")

#gets all of the days of the week for an item
def get_days_of_week(prompt):
    days = input(prompt).split()
    valid_days = {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'}
    if all(day in valid_days for day in days):
        return days
    else:
        print("Invalid days of the week. Please use full day names (e.g., Monday).")
        return get_days_of_week(prompt)

#how often an assignment is due
#should be changed to what day is the assignment due / future edits
def get_frequency(prompt):
    freq = input(prompt).lower()
    if freq in {'weekly', 'biweekly'}:
        return freq
    else:
        print("Invalid frequency. Please choose 'weekly' or 'biweekly'.")
        return get_frequency(prompt)

#gets estimated time of how long an assignment will take
def get_estimated_time(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def find_class(class_name, classes):
    size = len(classes)
    count = 0
    while count < size:
            if classes['name'] == class_name:
                return count
    return -1

def generate_schedule(semester_start, semester_end, classes, assignments, exams): #update for the specific arrays i want implemented
    calendar = {}

    current_date = semester_start
    while current_date <= semester_end:
        week_day = current_date.strftime('%A')
        calendar[current_date.strftime('%Y-%m-%d')] = []

        # Schedule classes
        for class_ in classes:
            if week_day in class_['days']:
                calendar[current_date.strftime('%Y-%m-%d')].append(f"{class_['name']} from {class_['start_time']} to {class_['end_time']}")

        # Schedule homework
        for assignment in assignments:
            if  week_day == assignment['due_day']:
                calendar[current_date.strftime('%Y-%m-%d')].append(f"Complete {assignment['name']} (Est. {assignment['estimated_time']} hours)")

        # Schedule exams
        for exam in exams:
            if current_date == exam['date']:
                calendar[current_date.strftime('%Y-%m-%d')].append(f"Study for {exam['name']} (Est. {exam['study_time']} hours)")

        current_date += timedelta(days=1)

    return calendar

#variable to keep track of the menu loop
run = 0

#defined variables for the program
classes = []
assignments = []
irregular = []
exams = []

#introduces the user to the program / welcome line
print("Welcome to the calendar for students \n")

#gets the start and end of the semester / should be the beginning of the calendar as well as the end of it
semester_start = get_date("Enter the start date of the semester (YYYY-MM-DD): ")
semester_end = get_date("Enter the end date of the semester (YYYY-MM-DD): ")

#start the menu loop for all actions involved in the calendar
while run >= 0:
    #menu options for the calendar
    print("\nWhat would you like to do")
    print("1. Add a class to the calendar")
    print("2. Remove a class from the calendar")
    print("3. Add a regular weekly assignment to the calendar")
    print("4. Add an irregular assignment to the calendar (one time)")
    print("5. Remove a weekly assignment")
    print("6. Remove an assignment (one time)")
    print("7. Add a midterm or final to the calendar")
    print("8. Remove a midterm or final from the calendar")
    print("9. Display current calendar") #would like it to be like an actual calendar or easy to read
    print("10. Download current schedule")
    print("11. Exit")
    run = int(input())

    #different statements for different menu options
    if run == 1:
        class_name = input("Enter the name of the class: ")
        class_days = get_days_of_week("Enter the days of the week the class occurs (separated by spaces): ")
        start_time = get_time("Enter the start time of the class (HH:MM): ")
        end_time = get_time("Enter the end time of the class (HH:MM): ")
        classes.append({
            'name': class_name,
            'days': class_days,
            'start_time': start_time,
            'end_time': end_time
        })

        calendar = generate_schedule(semester_start, semester_end, classes, assignments, exams)

    elif run == 2:
        class_name = input("Enter the name of the class you would like to remove: ")
        remove = find_class(class_name, classes)
        classes.pop(remove) #add error handling for classes that cannot be found
        
        calendar = generate_schedule(semester_start, semester_end, classes, assignments, exams)
    
    elif run == 3:
        assignment_name = input("What is the name of the assignment: ")
        assignment_due = input("What day of the week is the assignment due: ")
        assignment_ettd = input("How long will it take you to complete the assignment (in hours)")
        assignments.append({
            'name' : assignment_name,
            'due date' : assignment_due,
            'estimate' : assignment_ettd
        })
        
        calendar = generate_schedule(semester_start, semester_end, classes, assignments, exams)

    elif run == 4:
        assignment_name = input("What is the name of the assignment: ")
        assignment_due = input("What day of the week is the assignment due: ")
        assignment_ettd = input("How long will it take you to complete the assignment (in hours)")
        irregular.append({
            'name' : assignment_name,
            'due date' : assignment_due,
            'estimate' : assignment_ettd
        })  
        calendar = generate_schedule(semester_start, semester_end, classes, assignments, exams) #modify   
    
    elif run == 5:
        print("in progress1")
    
    elif run == 6:
        print("in progress2")

    elif run == 7:
        print("in progress3")

    elif run == 8:
        print("in progress4")
        
    elif run == 9:
        for date, events in sorted(calendar.items()):
            print(f"{date}:")
            for event in events:
                print(f"  - {event}")

    elif run == 10:
        print("in progress6")

    elif run == 11:
        print("in progress7")
    else:
            #fix error if two invalid inputs are used are after each other
            run = input("Invalid try another option \n")
