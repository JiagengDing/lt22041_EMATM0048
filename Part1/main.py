#!/usr/bin/python3
"""
@author: Jiageng Ding
@time: 2023-01-02
"""

from customer import *


def main():
    while (True):
        print("""
                ==== Money Transfer System ====
                1. Create an Account
                2. Login an Account
                Q. Quit
        """)
        choice = input("Enter choice: ")
        if choice.upper() == "Q":
            break
        elif (choice == "1"):
            Customer_Account.create_account()
        elif (choice == "2"):
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


if __name__ == '__main__':
    main()
