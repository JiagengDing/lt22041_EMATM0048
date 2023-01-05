#!/usr/bin/python3
"""
@author: Jiageng Ding
@time: 2023-01-02

This file contains all the classes about wallet needed for main.py file
"""

import csv
import os


class Wallets:
    fieldnames = ['id', 'kind', 'balance', 'customer_id']
    wallet_kinds = { # value-list 1.Withdraw 2.Deposit 3.Transfer to wallets 4.Transfer to other customers
        "Daily_Use": [1, 1, 1, 1],
        "Saving": [1, 1, 0, 0],
        "Holidays": [1, 1, 1, 0],
        "Mortgage": [0, 1, 0, 0]
    }

    def __init__(self, id, kind, balance, customer_id):
        self.id = id
        self.kind = kind
        self.balance = balance
        self.customer_id = customer_id

    @classmethod
    def create_wallet(cls, user):
        while True:
            print("""
                ==== Wallet Kinds ====
                1. Daily Use
                2. Saving
                3. Holidays
                4. Mortgage
                Q. Quit
                """)
            select = input(
                "Please enter the kind of wallet you want to create(Key Q to quit): "
            )
            kind = {
                "1": "Daily_Use",
                "2": "Saving",
                "3": "Holidays",
                "4": "Mortgage"
            }
            if select not in kind:
                print("Please enter the right number")
                continue
            kind_name = kind[select]
            if getattr(user, kind_name):
                print("You have already had this kind of wallet")
                continue
            id = cls.get_id()
            wallet = cls(id, kind, 0, user.id)
            setattr(user, kind_name, id)
            user.update_info()
            if not os.path.exists("wallets.csv"):
                with open("wallets.csv", "w") as f:
                    fieldnames = ["id", "kind", "balance", "customer_id"]
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow({
                        "id": id,
                        "kind": kind_name,
                        "balance": 0,
                        "customer_id": user.id
                    })
            else:
                with open("wallets.csv", "a") as f:
                    fieldnames = ["id", "kind", "balance", "customer_id"]
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writerow({
                        "id": id,
                        "kind": kind_name,
                        "balance": 0,
                        "customer_id": user.id
                    })
                print("Your wallet has been created:create_wallet")
            return wallet

    @classmethod
    def delete_wallet(cls, user):
        wallets = user.check_wallet()
        if not wallets:
            print("You don't have any wallet yet")
            return

        while True:
            wallets = user.check_wallet()
            for i, wallet in enumerate(wallets):
                print(f"{i}. {wallet.kind}")
            select = input(
                "Please enter the number of the wallet you want to delete(Key Q to quit): "
            )
            if select.upper() == "Q":
                break
            if not select.isdigit():
                print("Please enter the right number")
                continue
            select = int(select)
            wallet = wallets[select]
            with open("wallets.csv", "r") as f:
                reader = [i for i in csv.DictReader(f)]
                for row in reader:
                    if row["id"] == wallet.id:
                        reader.remove(row)
                        break
                with open("wallets.csv", "w") as fw:
                    fieldnames = ["id", "kind", "balance", "customer_id"]
                    writer = csv.DictWriter(fw, fieldnames=fieldnames)
                    writer.writeheader()
                    for row in reader:
                        writer.writerow(row)
                print("Your wallet has been deleted:delete_wallet")
                setattr(user, wallet.kind, None)
                user.update_info()

    @classmethod
    def get_id(cls):
        with open("wallets.csv", "r") as f:
            reader = csv.DictReader(f)
            wallets = [int(row["id"]) for row in reader if row["id"].isdigit()]
            if not wallets:
                return "2000"
            else:
                max_id = max(wallets)
        return max_id + 1

    @classmethod
    def get_wallet_info(cls, user):
        with open("wallets.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["customer_id"] == user.id:
                    return row

    def update_info(self):
        # find the row of the wallet
        new_rows = []
        with open("wallets.csv", "r") as f:
            reader = [i for i in csv.DictReader(f)]
            for row in reader:
                row = dict(row)
                if row["id"] == self.id:
                    row["balance"] = self.balance
                new_rows.append(row)
            # write to file
            with open("wallets.csv", "w") as fw:
                fieldnames = ["id", "kind", "balance", "customer_id"]
                writer = csv.DictWriter(fw, fieldnames=fieldnames)
                writer.writeheader()
                for row in new_rows:
                    writer.writerow(row)
            print("Your info has been updated:update_info")

    @classmethod
    def get_wallet_by_id(cls, id):
        with open("wallets.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["id"] == str(id):
                    return Wallets(row["id"], row["kind"], row["balance"],
                                   row["customer_id"])
            else:
                return None

    # check able to withdraw, deposit, trarsfer or not
    def is_able_to_withdraw(self):
        if self.wallet_kinds[self.kind][0]:
            return True
        else:
            return False

    def is_able_to_deposit(self):
        if self.wallet_kinds[self.kind][1]:
            return True
        else:
            return False

    def is_able_to_transfer_to_wallets(self):
        if self.wallet_kinds[self.kind][2]:
            return True
        else:
            return False

    def is_able_to_transfer_to_other_customers(self):
        if self.wallet_kinds[self.kind][3]:
            return True
        else:
            return False
