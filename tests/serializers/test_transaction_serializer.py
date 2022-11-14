from datetime import (
    date,
    datetime,
)
from unittest import TestCase

from model.transaction import Transaction
from serializers.transaction_serializer import TransactionSerializer


class TransactionSerializerTests(TestCase):
    def test_serialize(self):
        today = date.today()
        transaction = Transaction(1, today, -200.55)
        data = TransactionSerializer().serialize(transaction)
        self.assertDictEqual(
            data,
            {
                'id': transaction.id,
                'date': today.strftime('%Y-%m-%d'),
                'amount': transaction.amount,
            }
        )

    def test_serialize_all(self):
        today = date.today()
        transaction = Transaction(1, today, -200.55)
        another_transaction = Transaction(2, today, 100)
        data = TransactionSerializer().serialize_all([transaction, another_transaction])
        self.assertEqual(
            data,
            [{
                'id': transaction.id,
                'date': today.strftime('%Y-%m-%d'),
                'amount': transaction.amount,
            }, {
                'id': another_transaction.id,
                'date': today.strftime('%Y-%m-%d'),
                'amount': another_transaction.amount,
            },
            ]
        )

    def test_deserialize(self):
        date_string = '2022-11-10'
        data = {
            'id': 1,
            'date': date_string,
            'amount': -200.55,
        }
        transaction = TransactionSerializer().deserialize(data)
        self.assertEqual(transaction.id, data['id'])
        self.assertEqual(transaction.date, datetime.strptime(data['date'], '%Y-%m-%d'))
        self.assertEqual(transaction.amount, data['amount'])

    def test_deserialize_all(self):
        date_string = '2022-11-10'
        data = [
            {
                'id': 1,
                'date': date_string,
                'amount': -200.55,
            }, {
                'id': 2,
                'date': date_string,
                'amount': 100,
            },
        ]
        transactions = TransactionSerializer().deserialize_all(data)
        self.assertEqual(len(transactions), 2)
        transaction = transactions[0]
        self.assertEqual(transaction.id, data[0]['id'])
        self.assertEqual(transaction.date, datetime.strptime(data[0]['date'], '%Y-%m-%d'))
        self.assertEqual(transaction.amount, data[0]['amount'])
        transaction = transactions[1]
        self.assertEqual(transaction.id, data[1]['id'])
        self.assertEqual(transaction.date, datetime.strptime(data[1]['date'], '%Y-%m-%d'))
        self.assertEqual(transaction.amount, data[1]['amount'])
