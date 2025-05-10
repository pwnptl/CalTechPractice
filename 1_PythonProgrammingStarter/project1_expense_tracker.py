import csv
import datetime
import json
import os
from collections import defaultdict
from enum import Enum


class Category(Enum):
    FOOD = 1
    TRAVEL = 2
    GROCERY = 3
    ENTERTAINMENT = 4
    BILLS = 5
    OTHERS = 99


category_list = Category.__members__.keys()


def parse_category_from_str(category_str):
    if isinstance(category_str, int):
        for category in Category:
            if category.value == category_str:
                return category

    for category in Category:
        if category.name == category_str:
            return category

    raise ValueError


def get_expense_dict_from_string(expense):
    try:
        expense = json.loads(expense)
        parse_date_or_throw(str(expense['date']))
        date = str(expense['date'])
        category_str = parse_category_from_str(str(expense['category']))
        amount = float(expense['amount'])
        description = str(expense['description'])
        return {'date': date, 'category': category_str, 'amount': amount, 'description': description}

    except ValueError:
        return {}


def get_dict_from_data(date, category, amount, description):
    return {'date': date, 'category': category, 'amount': amount, 'description': description}


def parse_date_or_throw(date_str):
    datetime.datetime.strptime(date_str, "%Y-%m-%d")


def get_date_from_user():
    while True:
        date_string = input("Provide date (YYYY-MM-DD): ")
        try:
            parse_date_or_throw(date_string)
            return date_string
        except ValueError:
            print("invalid date provided")
            continue
    pass


def get_category_from_user():
    while True:
        try:
            print("Expense Categories:")
            for category in Category:
                print("\t", category.value, ":", category.name)
            category_from_user = input("enter category (default 99): ")
            if category_from_user == "":
                category_from_user = Category.OTHERS
                break
            elif category_from_user.isnumeric():
                category_from_user = Category(int(category_from_user))
                break
            else:
                found = False
                for category in Category:
                    if category.name == category_from_user:
                        category_from_user = category
                        found = True
                        break
                if found:
                    break
            print("invalid category entered")
            continue
        except ValueError:
            print("invalid category entered")
    print("Category chosen : ", category_from_user.name)
    return category_from_user


def get_amount_from_user():
    while True:
        try:
            amount_from_user = input("Enter Amount (without currency): ")
            return float(amount_from_user)
        except ValueError:
            print("Enter a valid amount")
    pass


def get_description_from_user():
    return input("Enter Description : ")
    pass


def get_data_for_add_expense():
    print("Provide Expense Details")

    date = get_date_from_user()
    category = get_category_from_user()
    amount = get_amount_from_user()
    description = get_description_from_user()
    expense = get_dict_from_data(date, category.name, amount, description)
    print("----------Your Expense summary-------------")
    print(expense)
    print("-------------------------------------------")
    return expense


expenses_file_name = "expenses.csv"
budget_file_name = "budget.csv"


def get_expenses_from_storage():
    try:
        expense_list = []
        with open(expenses_file_name, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['amount'] = float(row['amount'])  # Convert amount back to float
                expense_list.append(row)
        return expense_list
    except FileNotFoundError:
        return []


def put_expenses_in_storage(expenses):
    with open(expenses_file_name, 'w', newline='') as file:
        fieldnames = ['date', 'category', 'amount', 'description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for expense in expenses:
            writer.writerow(expense)
        file.flush()
        os.fsync(file.fileno())


def get_budget_from_storage():
    try:
        with open(budget_file_name) as file:
            return float(file.readline().strip())
    except FileNotFoundError:
        return 0.0
    except ValueError:
        return 0.0


def put_budget_in_storage(monthly_budget):
    with open(budget_file_name, 'w') as file:
        file.write(str(monthly_budget))

        file.flush()
        os.fsync(file.fileno())


def select_from_menu(menu_list):
    while True:
        print()
        print('-----------------------------')
        for menu_item in menu_list:
            print(menu_item[1])
        choice = input("---------> enter a choice: ")

        try:
            choice = int(choice)
            if 0 < choice <= len(menu_list):
                return menu_list[choice - 1][2]
        except ValueError:
            continue
    pass


def view_expenses(expense_list):
    print("{:<5} {:<12} {:<12} {:<15} {:<50}".format("#", "Date", "Amount", "Category", "Description"))
    for index, expense in enumerate(expense_list, start=1):
        print("{:<5} {:<12} {:<12} {:<15} {:<50}".format(
            index,
            expense['date'],
            f"{expense['amount']:.2f}",
            expense['category'],
            expense['description']
        ))


def add_expense(expense_list):
    expense = get_data_for_add_expense()
    expense_list.append(expense)


def group_expenses_by_month(expense_list):
    grouped_expenses = defaultdict(list)

    for expense in expense_list:
        date_obj = datetime.datetime.strptime(expense['date'], "%Y-%m-%d")
        year_month = date_obj.strftime("%Y-%m")

        grouped_expenses[year_month].append(expense)
    return grouped_expenses
    pass

def get_monthly_budget():
    monthly_budget = get_budget_from_storage()
    print('currently set monthly budget : ', monthly_budget)
    new_monthly_budget = input('enter new budget (enter for no change): ')
    if new_monthly_budget != '':
        try:
            monthly_budget = float(new_monthly_budget)
            put_budget_in_storage(monthly_budget)
        except ValueError:
            pass
    return monthly_budget


def track_budget(expense_list):
    monthly_budget = get_monthly_budget()

    grouped_expenses = group_expenses_by_month(expense_list)
    print_monthly_expense_budget(grouped_expenses, monthly_budget)
    pass


def print_monthly_expense_budget(grouped_expenses, monthly_budget):
    print('---------------------------------------------------------------------')
    print("{:<5} {:<12} {:<12} {:<15}".format("#", "Month", "Expense", "Remaining"))
    for index, grouped_expense_key in enumerate(grouped_expenses, start=1):
        this_month_expense = 0
        for expense in grouped_expenses[grouped_expense_key]:
            this_month_expense += expense['amount']
        remaining = monthly_budget - this_month_expense
        print("{:<5} {:<12} {:<12} {:<15}".format(index, grouped_expense_key, this_month_expense, remaining))
    print()


if __name__ == '__main__':

    expense_list = get_expenses_from_storage()
    menu_list = [
        (1, "1 . Add Expense", add_expense),
        (2, '2. View Expenses', view_expenses),
        (3, '3. Track Budget', track_budget),
        (4, '4. Save Expenses', put_expenses_in_storage),
        (5, '5. Exit', None)
    ]

    while True:
        function_to_execute = select_from_menu(menu_list)
        if function_to_execute is None:
            break
        function_to_execute(expense_list)

    put_expenses_in_storage(expense_list)
    print('Exiting after saving')
    pass
