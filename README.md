# Swiss-Hourly-Wage-Calculator

A calculator to calculate your hourly wage based on your salary, holidays, work hours, etc. This application uses the official data from Canton de Vaud 2024 for holidays and vacations.

## Features

- Calculate hourly wage for different roles: Teacher, Employee, and Freelance.
- Takes into account holidays and vacations.
- Allows customization of weekly work hours, monthly salary, number of monthly salaries, and additional hours for teachers.
- Simple and intuitive graphical user interface (GUI) built with Tkinter.
- For the teacher role, checks if a holiday occurs during vacations to avoid counting double non-working days.


## Requirements

- Python 3.x
- Tkinter (usually included with Python installations)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/AlexIn-Tech/Swiss-Hourly-Wage-Calculator.git
    cd Swiss-Hourly-Wage-Calculator
    ```

2. Ensure you have the required JSON file (`holidays_vacations_2024.json`) in the same directory as `mainGUI.py`.

## Usage

1. Run the application:
    ```bash
    python mainGUI.py
    ```

2. The GUI will open, allowing you to input the following details:
    - **Role**: Select your role (Teacher, Employee, Freelance).
    - **Net Monthly Salary (CHF)**: Enter your net monthly salary.
    - **Number of Monthly Salaries**: Enter the number of monthly salaries you receive per year.
    - **Weekly Hours**: Enter the number of hours you work per week.
    - **Additional Hours**: (Visible only for Teachers) Enter additional hours for preparation and correction.
    - **Vacation Weeks**: (Visible for Employees and Freelancers) Enter the number of vacation weeks.
    - **Include Official Holidays**: (Visible for Freelancers) Check if you want to include official holidays in the calculation.

3. Click on "Calculate Hourly Rate" to get your hourly rate.

4. Click on "Reset Values" to reset all fields to their default values.

## Example

![Screenshot](/img/Swiss-Hourly-Wage-Calculator.png)

## Data Source

The application uses the official data from Canton de Vaud 2024 for holidays and vacations. If you would like to change this information, edit the `holidays_vacations_2024.json` file.

https://www.vd.ch/formation/jours-feries-et-vacances-scolaires/jours-feries-et-vacances-scolaires-2024

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
