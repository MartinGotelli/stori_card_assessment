from datetime import datetime

from model.transaction import Transaction


class TransactionSerializer:
    def serialize(self, transaction):
        return {
            'id': transaction.id,
            'date': transaction.date.strftime('%Y-%m-%d'),
            'amount': transaction.amount,
        }

    def serialize_all(self, transactions):
        return [self.serialize(transaction) for transaction in transactions]

    def deserialize(self, data):
        date = datetime.strptime(data['date'], '%Y-%m-%d')
        return Transaction(data['id'], date, data['amount'])

    def deserialize_all(self, data_list):
        return [self.deserialize(data) for data in data_list]
