#!/usr/bin/python3
"""
@author: Jiageng Ding
@time: 2023-01-02

This file contains all the classes about customer needed for the main.py file
"""

import csv
import hashlib
import os


class Customer_Account:

    def __init__(self,
                 id,
                 name,
                 first_name,
                 age,
                 password,
                 country,
                 Daily_Use=None,
                 Saving=None,
                 Holidays=None,
                 Mortgage=None):
        self.id = id
        self.name = name
        self.first_name = first_name
        self.age = age
        self.password = password
        self.country = country
        self.Daily_Use = Daily_Use
        self.Saving = Saving
        self.Holidays = Holidays
        self.Mortgage = Mortgage

    @classmethod
    def create_account(cls):
        while True:
            name = input("Please enter your name(Key Q to quit): ")
            if name.upper() == "Q":
                break
            first_name = input("Please enter your first name: ")
            age = input("Please enter your age: ")
            password1 = input("Please enter your password: ")
            password = hashlib.md5(password1.encode()).hexdigest()
            country = input("Please enter your country: ")
            if all([
                    name.strip(),
                    first_name.strip(),
                    age.strip(),
                    password1.strip(),
                    country.strip()
            ]):
                break
            else:
                print("Please enter all the information")
        id = cls.get_id()
        with open("customer_account.csv", "a") as f:
            fieldnames = [
                'id', 'name', 'first_name', 'age', 'password', 'country',
                'Daily_Use', 'Saving', 'Holidays', 'Mortgage'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                "id": id,
                "name": name,
                "first_name": first_name,
                "age": age,
                "password": password,
                "country": country,
                "Daily_Use": None,
                "Saving": None,
                "Holidays": None,
                "Mortgage": None
            })
        print("Your account has been created")
        print("Your id is: ", id)

        return cls(id, name, first_name, age, password, country)

    @classmethod
    def login(cls):
        if not os.path.exists("customer_account.csv"):
            with open("customer_account.csv", "w") as f:
                fieldnames = [
                    'id', 'name', 'first_name', 'age', 'password', 'country',
                    'Daily_Use', 'Saving', 'Holidays', 'Mortgage'
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
        with open("customer_account.csv", "r") as f:
            reader = [i for i in csv.DictReader(f)]
            while True:
                id = input("Please enter your id(Key Q to break): ")
                if id.upper() == "Q":
                    return None
                password1 = input("Please enter your password: ")
                flag = False
                for row in reader:
                    if row["id"] == id:
                        flag = True
                        password1 = password1.encode()
                        # encry the password and compare it with the password in the file
                        password = hashlib.md5(password1).hexdigest()
                        if row["password"] == password:
                            return Customer_Account(
                                row["id"], row["name"], row["first_name"],
                                row["age"], row["password"], row["country"],
                                row["Daily_Use"], row["Saving"],
                                row["Holidays"], row["Mortgage"])
                        else:
                            print("Wrong password")
                if not flag:
                    print("Wrong id")

    def logout(self):
        user = None
        print("You have logged out")
        return user

    def check_wallet(self):
        res = []
        for kind in Wallets.wallet_kinds.keys():
            id = getattr(self, kind)
            if id:
                wallet = Wallets.get_wallet_by_id(id)
                res.append(wallet)

        return res

    def update_info(self):
        # find the row of the customer
        with open("customer_account.csv", "r") as f:
            reader = [i for i in csv.DictReader(f)]
            for row in reader:
                if row["id"] == self.id:
                    # update the row
                    row["name"] = self.name
                    row["first_name"] = self.first_name
                    row["age"] = self.age
                    row["password"] = self.password
                    row["country"] = self.country
                    row["Daily_Use"] = self.Daily_Use
                    row["Saving"] = self.Saving
                    row["Holidays"] = self.Holidays
                    break

            # write to file
            with open("customer_account.csv", "w") as fw:
                fieldnames = [
                    "id", 'name', 'first_name', 'age', 'password', 'country',
                    'Daily_Use', 'Saving', 'Holidays', 'Mortgage'
                ]
                writer = csv.DictWriter(fw, fieldnames=fieldnames)
                writer.writeheader()
                for row in reader:
                    writer.writerow(row)
            print("Your info has been updated:update_info")

    @classmethod
    def get_id(cls):
        if not os.path.exists("customer_account.csv"):
            return "1000"
        with open("customer_account.csv", "r") as f:
            reader = csv.DictReader(f)
            users = [int(row["id"]) for row in reader]
            if not users:
                return 1000
            else:
                max_id = max(users)
        return max_id + 1

    @classmethod
    def get_user_by_id(cls, id):
        with open("customer_account.csv", "r") as f:
            reader = [i for i in csv.DictReader(f)]
            for row in reader:
                if row["id"] == str(id):
                    return Customer_Account(row["id"], row["name"],
                                            row["first_name"], row["age"],
                                            row["password"], row["country"],
                                            row["Daily_Use"], row["Saving"],
                                            row["Holidays"], row["Mortgage"])
            else:
                return None
