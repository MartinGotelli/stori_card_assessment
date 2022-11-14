from datetime import date
from unittest import TestCase

from model.account import Account
from model.transaction import Transaction
from serializers.account_serializer import AccountSerializer
from serializers.transaction_serializer import TransactionSerializer


class AccountSerializerTests(TestCase):
    def test_serialize(self):
        today = date.today()
        credit = Transaction(1, today, 100)
        debit = Transaction(1, today, -100)
        account = Account(87, 'Test Account', {1: credit, 2: debit})
        data = AccountSerializer().serialize(account)
        self.assertDictEqual(
            data,
            {
                'id': account.id,
                'description': account.description,
                'transactions': TransactionSerializer().serialize_all(account.transactions())
            }
        )

    def test_deserialize(self):
        date_string = '2022-11-10'
        transactions_data = [
            {
                'id': 1,
                'date': date_string,
                'amount': 100,
            }, {
                'id': 2,
                'date': date_string,
                'amount': -100,
            },
        ]
        data = {
            'id': 87,
            'description': 'Test Account',
            'transactions': transactions_data
        }
        account = AccountSerializer().deserialize(data)
        self.assertEqual(account.id, data['id'])
        self.assertEqual(account.description, data['description'])
        transactions = account.transactions()
        expected_transactions = TransactionSerializer().deserialize_all(data['transactions'])
        self.assertEqual(len(transactions), 2)
        transaction = transactions[0]
        self.assertEqual(transaction.id, expected_transactions[0].id)
        self.assertEqual(transaction.date, expected_transactions[0].date)
        self.assertEqual(transaction.amount, expected_transactions[0].amount)
        transaction = transactions[1]
        self.assertEqual(transaction.id, expected_transactions[1].id)
        self.assertEqual(transaction.date, expected_transactions[1].date)
        self.assertEqual(transaction.amount, expected_transactions[1].amount)
