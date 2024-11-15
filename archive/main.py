import json
from datetime import datetime

# Load holidays and vacations from JSON
def load_holidays_and_vacations(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    holidays = [datetime.strptime(date, "%Y-%m-%d") for date in data["holidays"]]
    vacations = [
        (datetime.strptime(start, "%Y-%m-%d"), datetime.strptime(end, "%Y-%m-%d"))
        for start, end in data["vacations"]
    ]
    return holidays, vacations

# Function to calculate teacher's hourly rate
def calculate_teacher_hourly_rate(monthly_salary, weekly_hours, additional_hours, holidays, vacations):
    yearly_salary = monthly_salary * 13  # Include the 13th salary
    weekly_hours_total = weekly_hours + additional_hours
    vacation_weeks = sum([(end - start).days + 1 for start, end in vacations]) / 7
    holiday_weeks = len(holidays) / 7
    total_weeks_in_year = 52
    working_weeks = total_weeks_in_year - vacation_weeks - holiday_weeks
    total_work_hours_year = weekly_hours_total * working_weeks
    return yearly_salary / total_work_hours_year

# Function to calculate employee's hourly rate
def calculate_employee_hourly_rate(monthly_salary, weekly_hours, vacation_weeks, holidays):
    yearly_salary = monthly_salary * 13  # Include the 13th salary
    holiday_weeks = len(holidays) / 7  # Convert holidays to weeks
    total_weeks_in_year = 52
    working_weeks = total_weeks_in_year - vacation_weeks - holiday_weeks
    total_work_hours_year = weekly_hours * working_weeks
    return yearly_salary / total_work_hours_year

# Main program logic
def main():
    # Load data from JSON
    holidays, vacations = load_holidays_and_vacations("holidays_vacations_2024.json")

    role = input("Are you a teacher or an employee? ").strip().lower()
    monthly_salary = float(input("Enter your monthly salary (CHF): "))

    if role == "teacher":
        weekly_hours = float(input("Enter the number of hours you work per week: "))
        additional_hours = int(input("Enter additional hours per week for preparation and correction (e.g., 5 or 10): "))
        hourly_rate = calculate_teacher_hourly_rate(monthly_salary, weekly_hours, additional_hours, holidays, vacations)
        print(f"As a teacher, your hourly rate is: {hourly_rate:.2f} CHF/hour")
    elif role == "employee":
        weekly_hours = float(input("Enter your weekly working hours (e.g., 40, 50): "))
        vacation_weeks = int(input("Enter the number of vacation weeks per year (e.g., 4 or 5): "))
        hourly_rate = calculate_employee_hourly_rate(monthly_salary, weekly_hours, vacation_weeks, holidays)
        print(f"As an employee, your hourly rate is: {hourly_rate:.2f} CHF/hour")
    else:
        print("Invalid role entered. Please enter 'teacher' or 'employee'.")

# Run the program
if __name__ == "__main__":
    main()

# Note: This tool uses 2024 data loaded from a JSON file for holidays and vacations in the canton of Vaud, Switzerland.
