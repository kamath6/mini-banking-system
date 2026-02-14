import csv
import os
import random

ACCOUNTS_FILE = "accounts.csv"
TRANSACTIONS_FILE = "transactions.csv"


# ✅ Ensure CSV files exist with headers
def initialize_files():
    if not os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["AccountNo", "Name", "PIN", "Balance"])

    if not os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["AccountNo", "Type", "Amount"])


# ✅ Create Account
def create_account():
    name = input("Enter your name: ")
    pin = input("Set 4-digit PIN: ")

    account_no = str(random.randint(10000, 99999))
    balance = 0

    with open(ACCOUNTS_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([account_no, name, pin, balance])

    print(f"Account created successfully! Your Account Number is: {account_no}")


# ✅ Login
def login():
    account_no = input("Enter Account Number: ")
    pin = input("Enter PIN: ")

    with open(ACCOUNTS_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["AccountNo"] == account_no and row["PIN"] == pin:
                print("Login Successful!")
                return row

    print("Invalid Account Number or PIN.")
    return None


# ✅ Deposit
def deposit(user):
    amount = float(input("Enter amount to deposit: "))
    user["Balance"] = str(float(user["Balance"]) + amount)

    update_account(user)
    record_transaction(user["AccountNo"], "Deposit", amount)

    print("Deposit Successful!")


# ✅ Withdraw
def withdraw(user):
    amount = float(input("Enter amount to withdraw: "))

    if float(user["Balance"]) >= amount:
        user["Balance"] = str(float(user["Balance"]) - amount)
        update_account(user)
        record_transaction(user["AccountNo"], "Withdraw", amount)
        print("Withdrawal Successful!")
    else:
        print("Insufficient Balance!")


# ✅ Update Account in CSV
def update_account(updated_user):
    rows = []

    with open(ACCOUNTS_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["AccountNo"] == updated_user["AccountNo"]:
                rows.append(updated_user)
            else:
                rows.append(row)

    with open(ACCOUNTS_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["AccountNo", "Name", "PIN", "Balance"])
        writer.writeheader()
        writer.writerows(rows)


# ✅ Record Transactions
def record_transaction(account_no, t_type, amount):
    with open(TRANSACTIONS_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([account_no, t_type, amount])


# ✅ Delete Account
def delete_account(user):
    rows = []

    with open(ACCOUNTS_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["AccountNo"] != user["AccountNo"]:
                rows.append(row)

    with open(ACCOUNTS_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["AccountNo", "Name", "PIN", "Balance"])
        writer.writeheader()
        writer.writerows(rows)

    print("Account Deleted Successfully!")


# ✅ Main Menu
def main():
    initialize_files()

    while True:
        print("\n==== Mini Banking System ====")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            create_account()

        elif choice == "2":
            user = login()
            if user:
                while True:
                    print("\n1. Deposit")
                    print("2. Withdraw")
                    print("3. Check Balance")
                    print("4. Delete Account")
                    print("5. Logout")

                    option = input("Choose option: ")

                    if option == "1":
                        deposit(user)

                    elif option == "2":
                        withdraw(user)

                    elif option == "3":
                        print("Current Balance:", user["Balance"])

                    elif option == "4":
                        delete_account(user)
                        break

                    elif option == "5":
                        break

        elif choice == "3":
            print("Thank you for using Mini Banking System!")
            break

        else:
            print("Invalid Choice!")


if __name__ == "__main__":
    main()
