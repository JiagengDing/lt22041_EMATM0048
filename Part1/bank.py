"""
@author: Jiageng Ding
@time: 2023-01-02
"""

import csv

from customer import Customer_Account


def transfer_to_number(s):
    try:
        if float(s) >= 0:
            return True, round(float(s), 2)
        else:
            return False, "Invalid amount"
    except ValueError:
        return False, "Invalid amount"


class BankingSystem:
    fieldnames = ["id", "kind", "money", "customer_id"]

    @classmethod
    def add_record(cls, kind, money, customer_id):
        with open("bank_account.csv", "a") as f:
            writer = csv.DictWriter(f, fieldnames=cls.fieldnames)
            id = cls.get_id()
            writer.writerow({
                "id": id,
                "kind": kind,
                "money": money,
                "customer_id": customer_id
            })
            print("Your record has been added:add_record")

    @classmethod
    def deposit(cls, user):
        wallets = user.check_wallet()
        if not wallets:
            print("You don't have any wallet yet")
            return
        while True:
            for i, wallet in enumerate(wallets):
                print(f"{i}. {wallet.kind} - {wallet.balance}")
            select = input(
                "Please select the wallet you want to deposit(Key Q to quit): "
            )
            if select.upper() == "Q":
                break
            if select.isdigit() and 0 <= int(select) <= len(
                    wallets) - 1 and wallets[int(select)].is_able_to_deposit():
                wallet = wallets[int(select)]
            else:
                print("Please enter the right number")
                continue
            amount = input(
                "Please enter the amount you want to deposit(Key Q to quit): ")
            if amount.upper() == "Q":
                break
            if not transfer_to_number(amount)[0]:
                print("Please enter a number")
                continue
            balance = transfer_to_number(wallet.balance)[1]
            balance += transfer_to_number(amount)[1]
            wallet.balance = balance
            wallet.update_info()
            print("Your deposit has been completed")
            break

    @classmethod
    def withdraw(cls, user):
        # print every kind of wallet and the balance
        wallets = user.check_wallet()
        if not wallets:
            print("You don't have any wallet yet")
            return

        while True:
            amount = input(
                "Please enter the amount you want to withdraw(Key Q to quit): "
            )
            if amount.upper() == "Q":
                break
            if not transfer_to_number(amount)[0]:
                print("Please enter a number")
                continue
            wallets = user.check_wallet()
            for i, wallet in enumerate(wallets):
                print(f"{i}. {wallet.kind} - {wallet.balance}")
            flag = False
            for wallet in wallets:
                if wallet.is_able_to_withdraw() and transfer_to_number(wallet.balance)[1] >= \
                        transfer_to_number(amount)[1]:
                    flag = True
                    balance = transfer_to_number(
                        wallet.balance)[1] - transfer_to_number(amount)[1]
                    wallet.balance = balance
                    wallet.update_info()
                    print("Your withdraw has been completed")
                    break
            if not flag:
                print(
                    "You don't have enough money every kind of wallet or you can't withdraw from this wallet"
                )
                continue

    @classmethod
    def transfer_to_wallet(cls, user):
        wallets = user.check_wallet()
        if not wallets:
            print("You don't have any wallet yet")
            return
        from_wallet = None
        while True:
            amount = input(
                "Please enter the amount you want to transfer(Key Q to quit): "
            )
            if amount.upper() == "Q":
                print("Your transfer has been canceled")
                return
            if not transfer_to_number(amount)[0]:
                print(
                    "Please enter a number, and the number should be greater than 0"
                )
                continue
            amount = transfer_to_number(amount)[1]
            while True:
                print("from_wallet:")
                for i, wallet in enumerate(wallets):
                    print(f"{i}. {wallet.kind} - {wallet.balance}")
                select = input(
                    "Please select the wallet you want to transfer from(Key Q to quit): "
                )
                if select.upper() == "Q":
                    print("Your transfer has been canceled")
                    return
                if select.isdigit() and 0 <= int(
                        select) <= len(wallets) - 1 and wallets[int(select)]:
                    from_wallet = wallets[int(select)]
                    if transfer_to_number(from_wallet.balance)[1] >= amount * (
                            1 + 0.005
                    ) and from_wallet.is_able_to_transfer_to_wallets():
                        break
                    else:
                        print("amount+fee(0.5%)=:",
                              transfer_to_number(amount * (1 + 0.005))[1])
                        print(
                            "You don't have enough money or you can't transfer from this wallet"
                        )
                        continue
                else:
                    print("Please enter the right number")
                    continue

            while True:
                print("to_wallet:")
                for index, wallet in enumerate(wallets):
                    print(f"{index}: {wallet.kind} {wallet.balance}")
                select = input(
                    "Please select the wallet you want to transfer to(Key Q to quit): "
                )
                if select.upper() == "Q":
                    print("Your transfer has been canceled")
                    return

                if select.isdigit() and 0 <= int(
                        select) <= len(wallets) - 1 and wallets[int(select)]:
                    to_wallet = wallets[int(select)]
                    if from_wallet.id == to_wallet.id:
                        print("You can't transfer to the same wallet")
                        continue
                    if to_wallet.is_able_to_deposit():
                        from_wallet_balance = transfer_to_number(
                            from_wallet.balance)[1]
                        from_wallet_balance -= amount * (1 + 0.005)
                        from_wallet.balance = from_wallet_balance
                        from_wallet.update_info()

                        to_wallet_balance = transfer_to_number(
                            to_wallet.balance)[1]
                        to_wallet_balance += transfer_to_number(amount)[1]
                        to_wallet.balance = to_wallet_balance
                        to_wallet.update_info()
                        BankingSystem.add_record("transfer_to_wallet",
                                                 amount * 0.005, to_wallet.id)
                        print("Your transfer has been completed")
                    else:
                        print("You can't transfer to this wallet")
                        continue
                else:
                    print("Please enter the right number")
                    continue

    @classmethod
    def transfer_to_customer(cls, user):
        wallets = user.check_wallet()
        if not wallets:
            print("You don't have any wallet yet")
            return
        from_wallet = None
        to_user_wallet = None

        while True:
            for i, wallet in enumerate(wallets):
                print(f"{i}. {wallet.kind} - {wallet.balance}")
            select = input(
                "Please select the wallet you want to transfer from(Key Q to quit): "
            )
            if select.upper() == "Q":
                print("Your transfer has been canceled")
                return
            if select.isdigit() and 0 <= int(select) <= len(wallets) - 1:
                from_wallet = wallets[int(select)]
                if from_wallet.is_able_to_transfer_to_other_customers():
                    break
                else:
                    print("You can't transfer from this wallet")
                    continue
            else:
                print("Please enter the right number")
                continue
        while True:
            username = input(
                "Please enter the username you want to transfer to(Key Q to quit): "
            )
            if username.upper() == "Q":
                print("Your transfer has been canceled")
                return
            if not username.strip():
                continue
            if username == user.username:
                print("You can't transfer to yourself")
                continue
            to_user = Customer_Account.get_user_by_username(username)
            if not to_user:
                print("This user doesn't exist")
                continue
            to_user_wallets = to_user.check_wallet()
            flag = False
            for _wallet in to_user_wallets:
                if _wallet.is_able_to_deposit():
                    flag = True
                    to_user_wallet = _wallet
                    break

            if not flag:
                print("This user hava no wallet that can receive money")
                continue
            else:
                break

        while True:
            amount = input(
                "Please enter the amount you want to transfer(Key Q to quit): "
            )
            if amount.upper() == "Q":
                print("Your transfer has been canceled")
                return
            if not transfer_to_number(amount)[0]:
                print(
                    "Please enter a number, and the number should be greater than 0"
                )
                continue
            amount = transfer_to_number(amount)[1]
            if transfer_to_number(
                    from_wallet.balance)[1] >= amount * (1 + 0.015) and all(
                        [from_wallet, to_user_wallet]):
                from_wallet.balance = transfer_to_number(
                    from_wallet.balance)[1] - transfer_to_number(amount)[1]
                from_wallet.update_info()

                to_user_wallet_balance = transfer_to_number(
                    to_user_wallet.balance)[1] + transfer_to_number(amount)[1]
                to_user_wallet.balance = to_user_wallet_balance
                to_user_wallet.update_info()

                BankingSystem.add_record("transfer_to_customer",
                                         transfer_to_number(amount * 0.015)[1],
                                         from_wallet.id)
                print("Your transfer has been completed")
                return
            else:
                print("amount+fee(1.5%)=:",
                      transfer_to_number(amount * (1 + 0.015))[1])
                print("You don't have enough money in this wallet")
                continue

    @classmethod
    def get_id(cls):
        max_id = "3000"
        with open("bank_account.csv", "r") as f:
            reader = [i for i in csv.DictReader(f)]
            if reader:
                max_id = max(
                    [int(i["id"]) for i in reader if i["id"].isdigit()])
        return max_id + 1
