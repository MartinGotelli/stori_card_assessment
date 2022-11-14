class Transaction:
    def __init__(self, id, date, amount):
        self.id = id
        self.date = date
        self.amount = amount

    def is_from_month(self, month):
        return self.date.month == month

    def is_debit(self):
        return self.amount < 0

    def is_credit(self):
        return not self.is_debit()