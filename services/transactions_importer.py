from datetime import datetime

from model.transaction import Transaction


class TransactionsImporter:
    def __init__(self, account, accounts_manager):
        self.account = account
        self.accounts_manager = accounts_manager

    def process(self, file_name):
        with open(file_name, 'r') as file:
            lines = file.readlines()[0:-1]
            for line in lines:
                id, date_string, amount_string = line.split(',')
                date = datetime.strptime(date_string, '%Y-%m-%d')
                amount = float(amount_string)
                self.account.add_transaction(Transaction(id, date, amount))
        self.accounts_manager.save(self.account)
