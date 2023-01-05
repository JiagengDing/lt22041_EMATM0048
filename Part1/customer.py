#!/usr/bin/python3
"""
@author: Jiageng Ding
@time: 2023-01-02

This file contains all the classes about customer needed for the main.py file
"""

import csv
import hashlib
import os
import re

from wallet import Wallets


class Customer_Account:
    fieldnames = [
        'id', 'last_name', 'first_name', 'username', 'age', 'email',
        'password', 'password1', 'country', 'Daily_Use', 'Saving', 'Holidays',
        'Mortgage'
    ]

    def __init__(self,
                 id,
                 last_name,
                 first_name,
                 username,
                 age,
                 email,
                 password,
                 password1,
                 country,
                 Daily_Use=None,
                 Saving=None,
                 Holidays=None,
                 Mortgage=None):
        self.id = id
        self.last_name = last_name
        self.first_name = first_name
        self.username = username
        self.age = age
        self.password = password
        self.password1 = password1
        self.email = email
        self.country = country
        self.Daily_Use = Daily_Use
        self.Saving = Saving
        self.Holidays = Holidays
        self.Mortgage = Mortgage

    @classmethod
    def create_account(cls):
        while True:
            first_name = input("Please enter your first_name(Key Q to quit): ")
            while True:
                if first_name.upper() == "Q":
                    return
                last_name = input("Please enter your last name: ")
                username = first_name + last_name
                user = cls.get_user_by_username(username)
                if user:
                    print("The username already exists, please try again.")
                    continue
                else:
                    break
            while True:
                age = input("Please enter your age: ")
                if age.isdigit() and 0 < int(age) < 100:
                    break
                else:
                    print("Please enter a number(0~100)!")
            while True:
                password = input("Please enter your password: ")
                if 0 < len(password) < 10:
                    break
                else:
                    print("Password should be 10 characters or less!")
            while True:
                email = input("Please enter your email: ")
                # regex
                email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                if re.match(email_regex, email):
                    break
                else:
                    print("Please enter a valid email address!")
            password1 = hashlib.md5(password.encode()).hexdigest()
            country = input("Please enter your country: ")
            if all([
                    last_name.strip(),
                    first_name.strip(),
                    age.strip(),
                    password.strip(),
                    password1.strip(),
                    country.strip()
            ]):
                id = cls.get_id()
                with open("customer_account.csv", "a") as f:
                    fieldnames = [
                        'id', 'last_name', 'first_name', 'username', 'age',
                        'email', 'password', 'password1', 'country',
                        'Daily_Use', 'Saving', 'Holidays', 'Mortgage'
                    ]
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writerow({
                        "id": id,
                        "last_name": last_name,
                        "first_name": first_name,
                        "username": first_name + last_name,
                        "age": age,
                        "password": password,
                        "password1": password1,
                        "email": email,
                        "country": country,
                        "Daily_Use": None,
                        "Saving": None,
                        "Holidays": None,
                        "Mortgage": None
                    })
                print("Your account has been created")
                print("Your id is: ", id)

                return cls(id, last_name, first_name, username, age, email,
                           password, password1, country)
            else:
                print("Please enter all the information")

    @classmethod
    def login(cls):
        if not os.path.exists("customer_account.csv"):
            with open("customer_account.csv", "w") as f:
                fieldnames = [
                    'id', 'last_name', 'first_name', 'username', 'age',
                    'email', 'password', 'password1', 'country', 'Daily_Use',
                    'Saving', 'Holidays', 'Mortgage'
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
        with open("customer_account.csv", "r") as f:
            reader = [i for i in csv.DictReader(f)]
            while True:
                username = input(
                    "Please enter your username(Key Q to break): ")
                if username.upper() == "Q":
                    return None
                password = input("Please enter your password: ")
                flag = False
                for row in reader:
                    if row["username"] == username:
                        flag = True
                        password1 = password.encode()
                        # encrypt the password and compare it with the password in the file
                        password1 = hashlib.md5(password1).hexdigest()
                        if row["password1"] == password1:
                            return Customer_Account(
                                row["id"], row["last_name"], row["first_name"],
                                row["username"], row["age"], row["email"],
                                row["password"], row["password1"],
                                row["country"], row["Daily_Use"],
                                row["Saving"], row["Holidays"],
                                row["Mortgage"])
                        else:
                            print("Wrong password")
                if not flag:
                    print("Wrong username")

    @classmethod
    def logout(cls):
        print("You have logged out")

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
                if row["username"] == self.username:
                    # update the row
                    for key in row.keys():
                        row[key] = getattr(self, key)
                    break

            # write to file
            with open("customer_account.csv", "w") as fw:
                fieldnames = [
                    'id', 'last_name', 'first_name', 'username', 'age',
                    'email', 'password', 'password1', 'country', 'Daily_Use',
                    'Saving', 'Holidays', 'Mortgage'
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
            users = [int(row["id"]) for row in reader if row["id"].isdigit()]
            if not users:
                return 1000
            else:
                max_id = max(users)
        return max_id + 1

    @classmethod
    def get_user_by_username(cls, username):
        with open("customer_account.csv", "r") as f:
            reader = [i for i in csv.DictReader(f)]
            for row in reader:
                if row["username"] == username:
                    return Customer_Account(row["id"], row["last_name"],
                                            row["first_name"], row["username"],
                                            row["age"], row["email"],
                                            row["password"], row["password1"],
                                            row["country"], row["Daily_Use"],
                                            row["Saving"], row["Holidays"],
                                            row["Mortgage"])
            else:
                return None
