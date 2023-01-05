# lt22041_EMATM0048

This is a repository for the coursework assessment of the Software Development Programming and algorithms unit.
Part 1 is about building a banking system using OOP.

> GithubLink: https://github.com/JiagengDing/lt22041_EMATM0048

## Part1

This project contains 3 python file to define class (customer_account, wallet and banksystem), and a main.py file to launch & show menu. For this project, the classmethod is used in the definition of the class to enable it to be called without instantiation. ID starting from 1000 and 2000 respectively were used in order to distinguish between users and wallets. The library used is csv, os, re, and hashlib.


In the Customer_Account class, the methods of create_account, logg_in, log_out, check_wallet, update_info  are implemented. Moreover, get_user_by_username is defined to login with username rather than ID, and get_id is used to creat account.


In the Wallet class, the methods of create_wallet, delete_wallet, get_wallet_info, update_info are implemented. And get_id is used to create wallet with ID, get_wallet_by_id is used to select wallet. Moreover, is_able_to_withdraw(/deposit/transfer) methods is used to decide wallet function.


In the main.py file, firstly I defined a init_csv function to create csv file which is used to store customer/wallet/banksystem's information. And the main function is used to launch app and show menu. And if you want to exit this app or return to upper menu, you can enter q/Q.


For unanticipated input, the determination of whether it is a number and the search for existing user information are used respectively, and then prompting for re-entry.


I think some of the more remarkable aspects of this project include the use of a matrix to control the wallet function and the use of regular expressions to restrict email input. However, the encryption of user passwords via md5 did not complete the assignment requirement to define an encryption function.


- main.py: Run this file to launch banking system. Username is first_name+last_name(e.g jaggerding). Enter q to exit
- customer.py: The class of operating customer_accouts
- wallets.py: The class of operating wallets


- customer.csv: Record all customers' accounts
- wallets.csv: Record all wallets information
- bank_account.csv: Record bank system information

ToDo:

- [x] Change login ID to username
- [x] Add email information
- [ ] Add bank_system class
- [ ] Change md5 to self encrpt method
- [ ] Fix transfer bug

## Part2
