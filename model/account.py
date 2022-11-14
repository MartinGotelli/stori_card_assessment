class Account:
    def __init__(self, id, description, transactions_by_id=None):
        if transactions_by_id is None:
            transactions_by_id = {}
        self.id = id
        self.description = description
        self.transactions_by_id = transactions_by_id

    def add_transaction(self, transaction):
        # Transactions with same ID will override, this is to prevent repeated
        self.transactions_by_id[transaction.id] = transaction

    def transactions(self):
        return list(self.transactions_by_id.values())

    def balance(self):
        return sum([transaction.amount for transaction in self.transactions()])

    def transactions_on(self, month):
        return (transaction for transaction in self.transactions() if transaction.is_from_month(month))

    def transactions_amount_on(self, month):
        return len(list(self.transactions_on(month)))

    def debit_transactions_on(self, month):
        return [transaction for transaction in self.transactions_on(month) if transaction.is_debit()]

    def credit_transactions_on(self, month):
        return [transaction for transaction in self.transactions_on(month) if transaction.is_credit()]

    def average_debit_on(self, month):
        return self._average_amount(self.debit_transactions_on(month))

    def average_credit_on(self, month):
        return self._average_amount(self.credit_transactions_on(month))

    def _average_amount(self, transactions):
        size = len(transactions)
        if size > 0:
            sum_amount = sum([transaction.amount for transaction in transactions])
            average = sum_amount / size
        else:
            average = 0
        return round(average, 2)
