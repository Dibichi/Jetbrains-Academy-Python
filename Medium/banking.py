import sqlite3
import random

def sql():
    conn = sqlite3.connect('card.s3db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS card (
    id INTEGER NOT NULL, 
    number TEXT NOT NULL, 
    pin TEXT NOT NULL, 
    balance INTEGER DEFAULT 0)''')
    conn.commit()
    return conn, c

conn, c = sql()

c.execute('SELECT * FROM card')

class Menus:
    def main(self):
        print('''1. Create an account
2. Log into acount
0. Exit''')

        num = int(input())
        return num

    def log(self):
        print('''1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit''')

        num = int(input())
        return num

def luhn_algorithm(number):
    total = 0
    new_number = []
    for i, num in enumerate(number, start=1):
        num = int(num)
        if i % 2 != 0:
            num = num * 2
            if num > 9:
                num = num - 9

        new_number.append(str(num))

    for i in new_number:
        total += int(i)

    if total % 10 == 0:
        return True

def make_card():
    IIN = '400000'
    c.execute('''SELECT id FROM card''')
    all_ids = c.fetchall()
    while True:
        card_num = IIN + "%010d" % random.randint(0, 9999999999)
        new_id = int("%08d" % random.randint(0, 99999999))
        if luhn_algorithm(card_num) and (new_id not in all_ids):
            break

    card_pin = "%04d" % random.randint(0,9999)
    c.execute('''INSERT INTO card (id, number, pin) 
    VALUES (?, ?, ?)''', (new_id, card_num, card_pin))
    conn.commit()
    return card_num, card_pin

# All account choices for managing an account
class AccountChoices:
    def __init__(self, number, pin):
        self.card_number = number
        self.pin = pin
        self.balance = 0
        self.info = None
        self.add_money = None

    # Checks credentials and logs into account
    def login(self):
        c.execute('''SELECT * FROM card
        WHERE number = ? AND pin = ?''', (self.card_number, self.pin))
        self.info = c.fetchone()
        return self.info

    # Displays money for account
    def display_balance(self):
        self.balance = self.info[-1]
        print('\nBalance: ' + str(self.balance) + '\n')

    def add_income(self, money, acc=None):
        if acc:
            c.execute("""UPDATE card 
            SET balance = balance + ?
            WHERE number = ?""", (money, acc))

            c.execute("""UPDATE card 
            SET balance = balance - ?
            WHERE number = ?""", (money, self.card_number))

        else:
            c.execute("""UPDATE card 
            SET balance = balance + ?
            WHERE number = ?""", (money, self.card_number))

        conn.commit()
        self.login()

    def transfer_money(self):
        self.balance = self.info[-1]
        list_cards = []
        c.execute("SELECT number FROM card")
        all_cards = c.fetchall()
        for tups in all_cards:
            for card in tups:
                list_cards.append(card)

        transfer_account = input('Enter card number:\n')
        if transfer_account == self.card_number:
            print("You can't transfer money to the same account!\n")
        elif not luhn_algorithm(transfer_account):
            print('Probably you made mistake in the card number. Please try again!\n')
        elif transfer_account not in list_cards:
            print('Such a card does not exist.\n')
        else:
            transfer_amount = input('Enter how much money you want to transfer:\n')
            if int(transfer_amount) > self.balance:
                print('Not enough money!\n')
            else:
                self.add_income(transfer_amount, transfer_account)
                print('Success!\n')

    def close_account(self):
        current_card = (self.card_number,)
        c.execute("DELETE FROM card WHERE number = ?", current_card)
        conn.commit()

while True:
    user_num = Menus().main()
    print()

    if user_num == 1:
        print('Your card has been created')
        user_card, user_pin = make_card()
        print(f'Your card number:\n{user_card}')
        print(f'Your card PIN:\n{user_pin}\n')
        continue

    elif user_num == 2:
        user_card = input('Enter your card number:\n')
        user_pin = input('Enter your PIN:\n')
        account = AccountChoices(user_card, user_pin)
        account_info = account.login()
        if account_info:
            print('You have successfully logged in!\n')

            while True:
                user_num = Menus().log()
                if user_num == 1:
                    # For balance
                    account.display_balance()

                elif user_num == 2:
                    # for adding money
                    income = input('\nEnter income:\n')
                    account.add_income(income)

                elif user_num == 3:
                    # Transfer money
                    print('\nTransfer')
                    account.transfer_money()

                elif user_num == 4:
                    account.close_account()
                    print('The account has been closed!\n')
                    break

                elif user_num == 5:
                    print('Logging out...\n')
                    break

                elif user_num == 0:
                    print('Bye!')
                    exit()

                else:
                    print('Not one of the choices\n')

        else:
            print('Wrong card number or PIN!\n')

    else:
        print('Bye!')
        break
conn.close()
