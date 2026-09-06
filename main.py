import sqlite3
from datetime import datetime

# Connect to the database
connection = sqlite3.connect("expenses.db")
cursor = connection.cursor()


# Create the expenses table
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    description TEXT
)
""")

connection.commit()


# Add an expense
def add_expense():
    # amount validation
    while True:
        try:
            amount = float(input("Enter the amount: "))

            if amount <= 0:
                print("Amount must be greater than 0.")
                continue

            break

        except ValueError:
            print("Invalid amount. Please enter a number.")

    # category validation
    while True:
        category = input("Enter the category: ").strip()

        if category:
            break

        print("Category cannot be empty.")

    # date validation
    while True:
        date = input("Enter the date (YYYY-MM-DD): ").strip()

        try:
            datetime.strptime(date, "%Y-%m-%d")
            break

        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD.")

    # description
    description = input("Enter the description: ").strip()

    cursor.execute("""
    INSERT INTO expenses (date, category, amount, description)
    VALUES (?, ?, ?, ?)
    """, (date, category, amount, description))

    connection.commit()

    print("Expense added successfully!")
# View all expenses
def view_expenses():
    cursor.execute("SELECT * FROM expenses")

    expenses = cursor.fetchall()

    if not expenses:
        print("\nNo expenses found.")
        return

    print("\n===== Your Expenses =====")

    for expense in expenses:
        print(f"ID: {expense[0]}")
        print(f"Date: {expense[1]}")
        print(f"Category: {expense[2]}")
        print(f"Amount: ₹{expense[3]:.2f}")
        print(f"Description: {expense[4]}")
        print("------------------------")

# Delete an expense
def delete_expense():
    try:
        expense_id = int(input("Enter the ID of the expense to delete: "))

        cursor.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
        )

        connection.commit()

        if cursor.rowcount == 0:
            print("No expense found with that ID.")
        else:
            print("Expense deleted successfully!")

    except ValueError:
        print("Invalid ID. Please enter a number.")

# Edit an expense
def edit_expense():
    try:
        expense_id = int(input("Enter the ID of the expense to edit: "))

        cursor.execute(
            "SELECT * FROM expenses WHERE id = ?",
            (expense_id,)
        )

        expense = cursor.fetchone()

        if expense is None:
            print("No expense found with that ID.")
            return

        print("\n===== Edit Expense =====")
        print("1. Amount")
        print("2. Category")
        print("3. Date")
        print("4. Description")
        print("5. Cancel")

        choice = input("What do you want to change? ")

        if choice == "1":
            while True:
                try:
                    amount = float(input("Enter the new amount: "))

                    if amount <= 0:
                        print("Amount must be greater than 0.")
                        continue

                    break

                except ValueError:
                    print("Invalid amount. Please enter a number.")

            cursor.execute(
                "UPDATE expenses SET amount = ? WHERE id = ?",
                (amount, expense_id)
            )

        elif choice == "2":
            category = input("Enter the new category: ").strip()

            if not category:
                print("Category cannot be empty.")
                return

            cursor.execute(
                "UPDATE expenses SET category = ? WHERE id = ?",
                (category, expense_id)
            )

        elif choice == "3":
            while True:
                date = input("Enter the new date (YYYY-MM-DD): ").strip()

                try:
                    datetime.strptime(date, "%Y-%m-%d")
                    break

                except ValueError:
                    print("Invalid date. Please use YYYY-MM-DD.")

            cursor.execute(
                "UPDATE expenses SET date = ? WHERE id = ?",
                (date, expense_id)
            )

        elif choice == "4":
            description = input("Enter the new description: ").strip()

            cursor.execute(
                "UPDATE expenses SET description = ? WHERE id = ?",
                (description, expense_id)
            )

        elif choice == "5":
            print("Edit cancelled.")
            return

        else:
            print("Invalid choice.")
            return

        connection.commit()

        print("Expense updated successfully!")

    except ValueError:
        print("Invalid ID. Please enter a number.")

# Search expenses by category
def search_by_category():
    category = input("Enter the category to search: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    cursor.execute("""
    SELECT * FROM expenses
    WHERE LOWER(category) = LOWER(?)
    """, (category,))

    expenses = cursor.fetchall()

    if not expenses:
        print("No expenses found in that category.")
        return

    print("\nSearch Results:")

    for expense in expenses:
        print(expense)

# Show total spending
def total_spending():
    cursor.execute("SELECT SUM(amount) FROM expenses")

    total = cursor.fetchone()[0]

    if total is None:
        total = 0

    print(f"\nTotal Spending: ₹{total:.2f}")


# Show category-wise spending
def category_wise_spending():
    cursor.execute("""
    SELECT category, SUM(amount)
    FROM expenses
    GROUP BY category
    ORDER BY SUM(amount) DESC
    """)

    results = cursor.fetchall()

    if not results:
        print("\nNo expenses found.")
        return

    print("\n===== Category-wise Spending =====")

    for category, total in results:
        print(f"{category}: ₹{total:.2f}")

# Search expenses by exact date
def search_by_date():
    date = input("Enter the date (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date. Please use YYYY-MM-DD.")
        return

    cursor.execute("""
    SELECT * FROM expenses
    WHERE date = ?
    """, (date,))

    expenses = cursor.fetchall()

    if not expenses:
        print("No expenses found for that date.")
        return

    print("\n===== Expenses on", date, "=====")

    for expense in expenses:
        print(f"ID: {expense[0]}")
        print(f"Category: {expense[2]}")
        print(f"Amount: ₹{expense[3]:.2f}")
        print(f"Description: {expense[4]}")
        print("------------------------")


# Show monthly spending
def monthly_report():
    month = input("Enter month (YYYY-MM): ").strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month. Please use YYYY-MM.")
        return

    cursor.execute("""
    SELECT SUM(amount)
    FROM expenses
    WHERE date LIKE ?
    """, (month + "%",))

    total = cursor.fetchone()[0]

    if total is None:
        print(f"\nNo expenses found for {month}.")
        return

    print(f"\n===== Monthly Report: {month} =====")
    print(f"Total Spending: ₹{total:.2f}")

# Main menu
while True:
    print("\n===== Expense Tracker =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Delete Expense")
    print("4. Edit Expense")
    print("5. Search by Category")
    print("6. Total Expenses")
    print("7. Category-wise Spending")
    print("8. Search by Date")
    print("9. Monthly Report")
    print("10. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_expense()

    elif choice == "2":
        view_expenses()

    elif choice == "3":
        delete_expense()

    elif choice == "4":
        edit_expense()

    elif choice == "5":
        search_by_category()

    elif choice == "6":
        total_spending()

    elif choice == "7":
        category_wise_spending()

    elif choice == "8":
        search_by_date()

    elif choice == "9":
        monthly_report()

    elif choice == "10":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")


connection.close()