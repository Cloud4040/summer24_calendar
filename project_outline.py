import json
import csv
from datetime import datetime, timedelta

def get_date(prompt):
    while True:
        try:
            return datetime.strptime(input(prompt), '%Y-%m-%d')
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def get_time(prompt):
    while True:
        try:
            return datetime.strptime(input(prompt), '%H:%M').time()
        except ValueError:
            print("Invalid time format. Please use HH:MM.")

def get_days_of_week(prompt):
    days = input(prompt).split()
    valid_days = {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'}
    if all(day in valid_days for day in days):
        return days
    else:
        print("Invalid days of the week. Please use full day names (e.g., Monday).")
        return get_days_of_week(prompt)

def get_frequency(prompt):
    freq = input(prompt).lower()
    if freq in {'weekly', 'biweekly'}:
        return freq
    else:
        print("Invalid frequency. Please choose 'weekly' or 'biweekly'.")
        return get_frequency(prompt)

def get_estimated_time(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")



# Step 1: Semester Dates
semester_start = get_date("Enter the start date of the semester (YYYY-MM-DD): ")
semester_end = get_date("Enter the end date of the semester (YYYY-MM-DD): ")

# Step 2: Classes
num_classes = int(input("Enter the number of classes: "))
classes = []

for _ in range(num_classes):
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

# Step 3: Homework Assignments
num_assignments = int(input("Enter the number of regular homework assignments: "))
assignments = []

for _ in range(num_assignments):
    assignment_name = input("Enter the name of the assignment: ")
    frequency = get_frequency("Is this assignment weekly or biweekly? ")
    due_day = input("Enter the due day of the week for the assignment: ")
    estimated_time = get_estimated_time("Enter the estimated time to complete the assignment (in hours): ")
    assignments.append({
        'name': assignment_name,
        'frequency': frequency,
        'due_day': due_day,
        'estimated_time': estimated_time
    })

# Step 4: Midterms and Finals
num_exams = int(input("Enter the number of midterms and finals: "))
exams = []

for _ in range(num_exams):
    exam_name = input("Enter the name of the exam: ")
    exam_date = get_date("Enter the date of the exam (YYYY-MM-DD): ")
    study_time = get_estimated_time("Enter the estimated study time required (in hours): ")
    exams.append({
        'name': exam_name,
        'date': exam_date,
        'study_time': study_time
    })

# Step 5: Generate Calendar (simple representation)
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
        if assignment['frequency'] == 'weekly' and week_day == assignment['due_day']:
            calendar[current_date.strftime('%Y-%m-%d')].append(f"Complete {assignment['name']} (Est. {assignment['estimated_time']} hours)")
        elif assignment['frequency'] == 'biweekly' and week_day == assignment['due_day']:
            start_of_week = (current_date - timedelta(days=current_date.weekday()))
            if (current_date - start_of_week).days % 14 == 0:
                calendar[current_date.strftime('%Y-%m-%d')].append(f"Complete {assignment['name']} (Est. {assignment['estimated_time']} hours)")

    # Schedule exams
    for exam in exams:
        if current_date == exam['date']:
            calendar[current_date.strftime('%Y-%m-%d')].append(f"Study for {exam['name']} (Est. {exam['study_time']} hours)")

    current_date += timedelta(days=1)

# Enhanced Calendar Display
for date, events in sorted(calendar.items()):
    print(f"{date}:")
    for event in events:
        print(f"  - {event}")

# Save to CSV
with open('calendar.csv', 'w', newline='') as csvfile:
    fieldnames = ['Date', 'Events']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for date, events in calendar.items():
        writer.writerow({'Date': date, 'Events': "; ".join(events)})

# Save to JSON
with open('calendar.json', 'w') as jsonfile:
    json.dump(calendar, jsonfile, indent=4)

print("Calendar saved to calendar.csv and calendar.json")
