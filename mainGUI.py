import json
from datetime import datetime, timedelta
import os
import tkinter as tk
from tkinter import messagebox
import sys

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
def calculate_teacher_hourly_rate(monthly_salary, monthly_salaries, weekly_hours, additional_hours, holidays, vacations):
    yearly_salary = monthly_salary * monthly_salaries  # Include the specified number of salaries
    weekly_hours_total = weekly_hours + additional_hours

    # Create sets of holiday dates and vacation dates
    holiday_dates = set(holidays)
    vacation_dates = set()
    for start, end in vacations:
        current_date = start
        while current_date <= end:
            vacation_dates.add(current_date)
            current_date += timedelta(days=1)

    # Calculate the number of overlapping days
    overlapping_days = holiday_dates & vacation_dates
    overlapping_days_count = len(overlapping_days)

    # Calculate vacation weeks and holiday weeks, accounting for overlap
    total_vacation_days = sum([(end - start).days + 1 for start, end in vacations])
    vacation_weeks = (total_vacation_days - overlapping_days_count) / 7
    holiday_weeks = (len(holidays) - overlapping_days_count) / 7

    total_weeks_in_year = 52
    working_weeks = total_weeks_in_year - vacation_weeks - holiday_weeks
    total_work_hours_year = weekly_hours_total * working_weeks
    return yearly_salary / total_work_hours_year

# Function to calculate employee's hourly rate
def calculate_employee_hourly_rate(monthly_salary, monthly_salaries, weekly_hours, vacation_weeks, holidays):
    yearly_salary = monthly_salary * monthly_salaries  # Include the specified number of salaries
    holiday_weeks = len(holidays) / 7  # Convert holidays to weeks
    total_weeks_in_year = 52
    working_weeks = total_weeks_in_year - vacation_weeks - holiday_weeks
    total_work_hours_year = weekly_hours * working_weeks
    return yearly_salary / total_work_hours_year

# Function to calculate freelance's hourly rate
def calculate_freelance_hourly_rate(monthly_salary, monthly_salaries, weekly_hours, vacation_weeks, include_holidays, holidays):
    yearly_salary = monthly_salary * monthly_salaries  # Include the specified number of salaries
    holiday_weeks = len(holidays) / 7 if include_holidays else 0
    total_weeks_in_year = 52
    working_weeks = total_weeks_in_year - vacation_weeks - holiday_weeks
    total_work_hours_year = weekly_hours * working_weeks
    return yearly_salary / total_work_hours_year

# Function to handle the calculation and display the result
def calculate_rate():
    role = role_var.get().strip().lower()
    try:
        monthly_salary = float(monthly_salary_entry.get())
        monthly_salaries = int(monthly_salaries_entry.get())
        weekly_hours = float(weekly_hours_entry.get())
        if role == "teacher":
            additional_hours = int(additional_hours_entry.get())
            hourly_rate = calculate_teacher_hourly_rate(monthly_salary, monthly_salaries, weekly_hours, additional_hours, holidays, vacations)
            messagebox.showinfo("Hourly Rate", f"As a teacher, your hourly rate is: {hourly_rate:.2f} CHF/hour")
        elif role == "employee":
            vacation_weeks = int(vacation_weeks_entry.get())
            hourly_rate = calculate_employee_hourly_rate(monthly_salary, monthly_salaries, weekly_hours, vacation_weeks, holidays)
            messagebox.showinfo("Hourly Rate", f"As an employee, your hourly rate is: {hourly_rate:.2f} CHF/hour")
        elif role == "freelance":
            vacation_weeks = int(vacation_weeks_entry.get())
            include_holidays = include_holidays_var.get()
            hourly_rate = calculate_freelance_hourly_rate(monthly_salary, monthly_salaries, weekly_hours, vacation_weeks, include_holidays, holidays)
            messagebox.showinfo("Hourly Rate", f"As a freelance, your hourly rate is: {hourly_rate:.2f} CHF/hour")
        else:
            messagebox.showerror("Error", "Invalid role entered. Please select 'teacher', 'employee', or 'freelance'.")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")

# Function to update the visibility of input fields based on the selected role
def update_visibility():
    role = role_var.get().strip().lower()
    if role == "teacher":
        # set_default_value(weekly_hours_entry, "21")
        # set_default_value(monthly_salaries_entry, "13")
        additional_hours_label.grid()
        additional_hours_entry.grid()
        vacation_weeks_label.grid_remove()
        vacation_weeks_entry.grid_remove()
        include_holidays_label.grid_remove()
        include_holidays_check.grid_remove()
    elif role == "employee":
        # set_default_value(weekly_hours_entry, "40")
        # set_default_value(monthly_salaries_entry, "13")
        additional_hours_label.grid_remove()
        additional_hours_entry.grid_remove()
        vacation_weeks_label.grid()
        vacation_weeks_entry.grid()
        include_holidays_label.grid_remove()
        include_holidays_check.grid_remove()
    elif role == "freelance":
        # (weekly_hours_entry, "40")
        # set_default_value(monthly_salaries_entry, "12")
        additional_hours_label.grid_remove()
        additional_hours_entry.grid_remove()
        vacation_weeks_label.grid()
        vacation_weeks_entry.grid()
        include_holidays_label.grid()
        include_holidays_check.grid()
    else:
        additional_hours_label.grid_remove()
        additional_hours_entry.grid_remove()
        vacation_weeks_label.grid_remove()
        vacation_weeks_entry.grid_remove()
        include_holidays_label.grid_remove()
        include_holidays_check.grid_remove()

# Function to set default value in entry fields
def set_default_value(entry, default_value):
    if entry.get() == "" or entry.cget("fg") == "grey":
        entry.delete(0, tk.END)
        entry.insert(0, default_value)
        entry.config(fg='grey')

# Function to handle focus in event
def on_focus_in(event, default_value):
    if event.widget.get() == default_value and event.widget.cget("fg") == "grey":
        event.widget.delete(0, tk.END)
        event.widget.config(fg='black')

# Function to handle focus out event
def on_focus_out(event, default_value):
    if event.widget.get() == "":
        event.widget.insert(0, default_value)
        event.widget.config(fg='grey')

# Function to reset values to default
def reset_values():
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Load data from JSON
file_path = os.path.join(os.path.dirname(__file__), "holidays_vacations_2024.json")
holidays, vacations = load_holidays_and_vacations(file_path)

# Create the main window
root = tk.Tk()
root.title("Swiss Hourly Wage Calculator")
root.geometry("1000x600")  # Set a fixed size for the window

# Create and place the widgets
tk.Label(root, text="Role:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
role_var = tk.StringVar(value="teacher")
tk.Radiobutton(root, text="Teacher", variable=role_var, value="teacher", command=update_visibility).grid(row=0, column=1, padx=10, pady=5, sticky="w")
tk.Radiobutton(root, text="Employee", variable=role_var, value="employee", command=update_visibility).grid(row=0, column=2, padx=10, pady=5, sticky="w")
tk.Radiobutton(root, text="Freelance", variable=role_var, value="freelance", command=update_visibility).grid(row=0, column=3, padx=10, pady=5, sticky="w")

tk.Label(root, text="Net Monthly Salary (CHF):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
monthly_salary_entry = tk.Entry(root)
monthly_salary_entry.insert(0, "6000")
monthly_salary_entry.config(fg='grey')
monthly_salary_entry.bind("<FocusIn>", lambda event: on_focus_in(event, "6000"))
monthly_salary_entry.bind("<FocusOut>", lambda event: on_focus_out(event, "6000"))
monthly_salary_entry.grid(row=1, column=1, padx=10, pady=5, columnspan=3, sticky="w")

tk.Label(root, text="Number of Monthly Salaries:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
monthly_salaries_entry = tk.Entry(root)
monthly_salaries_entry.insert(0, "13")
monthly_salaries_entry.config(fg='grey')
monthly_salaries_entry.bind("<FocusIn>", lambda event: on_focus_in(event, "13"))
monthly_salaries_entry.bind("<FocusOut>", lambda event: on_focus_out(event, "13"))
monthly_salaries_entry.grid(row=2, column=1, padx=10, pady=5, columnspan=3, sticky="w")

tk.Label(root, text="Weekly Hours:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
weekly_hours_entry = tk.Entry(root)
weekly_hours_entry.insert(0, "40")
weekly_hours_entry.config(fg='grey')
weekly_hours_entry.bind("<FocusIn>", lambda event: on_focus_in(event, "40"))
weekly_hours_entry.bind("<FocusOut>", lambda event: on_focus_out(event, "40"))
weekly_hours_entry.grid(row=3, column=1, padx=10, pady=5, columnspan=3, sticky="w")

additional_hours_label = tk.Label(root, text="Additional Hours:")
additional_hours_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
additional_hours_entry = tk.Entry(root)
additional_hours_entry.insert(0, "5")
additional_hours_entry.config(fg='grey')
additional_hours_entry.bind("<FocusIn>", lambda event: on_focus_in(event, "5"))
additional_hours_entry.bind("<FocusOut>", lambda event: on_focus_out(event, "5"))
additional_hours_entry.grid(row=4, column=1, padx=10, pady=5, columnspan=3, sticky="w")

vacation_weeks_label = tk.Label(root, text="Vacation Weeks:")
vacation_weeks_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
vacation_weeks_entry = tk.Entry(root)
vacation_weeks_entry.insert(0, "4")
vacation_weeks_entry.config(fg='grey')
vacation_weeks_entry.bind("<FocusIn>", lambda event: on_focus_in(event, "4"))
vacation_weeks_entry.bind("<FocusOut>", lambda event: on_focus_out(event, "4"))
vacation_weeks_entry.grid(row=5, column=1, padx=10, pady=5, columnspan=3, sticky="w")

include_holidays_var = tk.BooleanVar()
include_holidays_label = tk.Label(root, text="Include Official Holidays:")
include_holidays_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
include_holidays_check = tk.Checkbutton(root, variable=include_holidays_var)
include_holidays_check.grid(row=6, column=1, padx=10, pady=5, columnspan=3, sticky="w")

tk.Button(root, text="Calculate Hourly Rate", command=calculate_rate).grid(row=7, column=0, columnspan=2, pady=10)
tk.Button(root, text="Reset Values", command=reset_values).grid(row=7, column=2, columnspan=2, pady=10)

disclaimer_label = tk.Label(root, text="* Using Canton de Vaud 2024 official data about holidays and vacations.\nIf you would like to change this information, edit the JSON file.", font=("Arial", 8, "italic"))
disclaimer_label.grid(row=8, column=0, columnspan=4, pady=10)

# Initialize the visibility of input fields
update_visibility()

# Run the main event loop
root.mainloop()