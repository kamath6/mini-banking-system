import csv
import os
import random

ACCOUNTS_FILE = "accounts.csv"
TRANSACTIONS_FILE = "transactions.csv"


# Ensure files exist
def initialize_files():
    if not os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["AccountNo", "Name", "PIN", "Balance"])

    if not os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["AccountNo", "Type", "Amount"])


def generate_account_number():
    return random.randint(10000, 99999)


def create_account():
    name = input("Enter your name: ")
    pin = input("Set 4-digit PIN: ")

    if len(pin) != 4 or not pin.isdigit():
        print("Invalid PIN.\n")
        return

    account_no = generate_account_number()

    with open(ACCOUNTS_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([account_no, name, pin, 0])

    print(f"Account created successfully! Account No: {account_no}\n")


def login():
    account_no = input("Enter Account Number: ")
    pin = input("Enter PIN: ")

    with open(ACCOUNTS_FILE, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["AccountNo"] == account_no and row["PIN"] == pin:
                print("Login Successful!\n")
                return row

    print("Invalid credentials.\n")
    return None


def update_balance(account_no, new_balance):
    rows = []

    with open(ACCOUNTS_FILE, "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    for row in rows:
        if row["AccountNo"] == account_no:
            row["Balance"] = new_balance

    with open(ACCOUNTS_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["AccountNo", "Name", "PIN", "Balance"])
        writer.writeheader()
        writer.writerows(rows)


def record_transaction(account_no, t_type, amount):
    with open(TRANSACTIONS_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([account_no, t_type, amount])


def banking_menu(user):
    account_no = user["AccountNo"]
    balance = float(user["Balance"])

    while True:
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Delete Account")
        print("5. Logout")

        choice = input("Choose option: ")

        if choice == "1":
            print(f"Balance: ₹{balance}\n")

        elif choice == "2":
            amount = float(input("Enter amount: "))
            balance += amount
            update_balance(account_no, balance)
            record_transaction(account_no, "Deposit", amount)
            print("Deposit Successful!\n")

        elif choice == "3":
            amount = float(input("Enter amount: "))
            if amount > balance:
                print("Insufficient Balance.\n")
            else:
                balance -= amount
                update_balance(account_no, balance)
                record_transaction(account_no, "Withdraw", amount)
                print("Withdrawal Successful!\n")

        elif choice == "4":
            confirm = input("Are you sure? (yes/no): ")
            if confirm.lower() == "yes":
                delete_account(account_no)
                break

        elif choice == "5":
            break

        else:
            print("Invalid choice.\n")


def delete_account(account_no):
    rows = []

    with open(ACCOUNTS_FILE, "r") as file:
        reader = csv.DictReader(file)
        rows = [row for row in reader if row["AccountNo"] != account_no]

    with open(ACCOUNTS_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["AccountNo", "Name", "PIN", "Balance"])
        writer.writeheader()
        writer.writerows(rows)

    print("Account Deleted Successfully!\n")


def main():
    initialize_files()

    while True:
        print("=== Mini Banking System ===")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            create_account()

        elif choice == "2":
            user = login()
            if user:
                banking_menu(user)

        elif choice == "3":
            break

        else:
            print("Invalid option.\n")


if __name__ == "__main__":
    main()
