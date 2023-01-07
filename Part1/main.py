#!/usr/bin/python3
"""
@author: Jiageng Ding
@time: 2023-01-02
"""
import csv
import os

from customer import Customer_Account
from wallet import Wallets
from bank import BankingSystem


def init_csv():
    if not os.path.exists("customer_account.csv"):
        with open("customer_account.csv", "w") as f:
            csv_writer = csv.DictWriter(f,
                                        fieldnames=Customer_Account.fieldnames)
            csv_writer.writeheader()
    if not os.path.exists("wallets.csv"):
        with open("wallets.csv", "w") as f:
            csv_writer = csv.DictWriter(f, fieldnames=Wallets.fieldnames)
            csv_writer.writeheader()
    if not os.path.exists("bank_account.csv"):
        with open("bank_account.csv", "w") as f:
            csv_writer = csv.DictWriter(f, fieldnames=BankingSystem.fieldnames)
            csv_writer.writeheader()


def main():
    init_csv()
    while True:
        print("""
                ==== Money Transfer System ====
                1. Create an Account
                2. Login an Account
                Q. Quit
        """)
        choice = input("Enter choice: ")
        if choice.upper() == "Q":
            return
        elif choice == "1":
            Customer_Account.create_account()
        elif choice == "2":
            user = Customer_Account.login()
            if user:
                while True:
                    print("""
                    ==== Money Transfer System ====
                    1. Check Wallets
                    2. Create Wallets
                    3. Deposit
                    4. Withdraw
                    5. Transfer to Wallets
                    6. Transfer to Other Customers
                    7. Delete Wallet
                    Q. Logout
                    """)
                    choice = input("Enter choice: ")
                    if choice == "1":
                        wallets = user.check_wallet()
                        if not wallets:
                            print("You don't have any wallet yet")
                            continue
                        for index, wallet in enumerate(wallets):
                            print(f"{index}: {wallet.kind} {wallet.balance}")
                    elif choice == "2":
                        Wallets.create_wallet(user)
                    elif choice == "3":
                        BankingSystem.deposit(user)
                    elif choice == "4":
                        BankingSystem.withdraw(user)
                    elif choice == "5":
                        BankingSystem.transfer_to_wallet(user)
                    elif choice == "6":
                        BankingSystem.transfer_to_customer(user)
                    elif choice == "7":
                        Wallets.delete_wallet(user)
                    elif choice.upper() == "Q":
                        Customer_Account.logout()
                        break
                    else:
                        print("Invalid choice")
        else:
            print("Invalid choice")


if __name__ == '__main__':
    main()
