# lt22041_EMATM0048

This is a repository for the coursework assessment of the Software Development Programming and algorithms unit.
Part 1 is about building a banking system using OOP.

> GithubLink: https://github.com/JiagengDing/lt22041_EMATM0048

## Part1

This project contains 3 python file to define class (customer_account, wallet and banksystem), and a main.py file to launch & show menu. For this project, the classmethod is used in the definition of the class to enable it to be called without instantiation. ID starting from 1000 and 2000 respectively were used in order to distinguish between users and wallets. The library used is csv, os, re, and hashlib.


In the Customer_Account class, the methods of create_account, logg_in, log_out, check_wallet, update_info  are implemented.
The create_accout classmethod could initiate a customer account with password, unique username and other info, and then write it in customer.csv file.
Moreover, get_user_by_username is defined to login with username rather than ID, and get_id is used to create account ID(start from 1000).


In the Wallet class, the methods of create_wallet, delete_wallet, get_wallet_info, update_info are implemented. The create_wallet classmethod could show sub menu, and then initiate a wallet with user ID, wallet kind and initial balance is 0. And get_id is used to create wallet ID(start from 2000), get_wallet_by_id is used to select wallet. Moreover, is_able_to_withdraw(/deposit/transfer) methods is used to decide wallet function.

In the BankingSystem account, I defined a transfer_to_number function to transform deposit/withdraw/transfer amount to 2 decimal places (If it is not a number, system will prompt to re-enter). The classmethod add_record and get_id are used to record bank system's income information. The classmethod deposit and withdraw are used to implement the deposit and withdraw function.
And the transfer_to_wallet & transfer_to_customer function are used to implement transfer and charge by bank.
In these classmethod, they use check_wallet method in customer_account class and get wallet info firstly.


In the main.py file, I defined a init_csv function to create csv file firstly which is used to store customer/wallet/banksystem's information. And the main function is used to launch app and show menu. If you want to exit this app or return to upper menu, you can enter q/Q.


For unanticipated input, the determination of whether it is a number and the search for existing user information are used respectively, and then prompting for re-entry.


I think some of the more remarkable aspects of this project include the use of a matrix to control the wallet function and the use of regular expressions to restrict email input. However, the password encryption method via md5 did not complete the assignment requirement.


- main.py: Run this file to launch banking system. Username is first_name+last_name(e.g jaggerding). Enter q to exit
- customer.py: The class of operating customer_accouts
- wallets.py: The class of operating wallets


- customer.csv: Record all customers' accounts
- wallets.csv: Record all wallets information
- bank_account.csv: Record bank system information

ToDo:

- [x] Change login ID to username
- [x] Add email information
- [x] Add bank_system class
- [x] Test this system
- [ ] Change md5 to other encrypt method
- [x] Fix bug after transfer finished. (It need user enter q to finish)

## Part2

In Part 2, I crawled some transaction data from Bitstamp, and performed data cleaning and analysis.
Details of Part 2 are displayed in Part2/Part2.ipynb.
