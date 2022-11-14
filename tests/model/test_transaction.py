import unittest
from datetime import (
    date,
    datetime,
)

from model.transaction import Transaction


class TransactionTests(unittest.TestCase):
    def test_creation(self):
        id = 87
        today = datetime.today()
        amount = -100
        transaction = Transaction(id, today, amount)
        self.assertEqual(transaction.id, id)
        self.assertEqual(transaction.date, today)
        self.assertEqual(transaction.amount, amount)

    def test_is_from_month(self):
        november_2022 = date(2022, 11, 10)
        transaction = Transaction(1, november_2022, 100)
        self.assertTrue(transaction.is_from_month(11))
        self.assertFalse(transaction.is_from_month(1))

    def test_is_debit(self):
        today = datetime.today()
        debit_transaction = Transaction(1, today, -100)
        credit_transaction = Transaction(2, today, 100)
        self.assertTrue(debit_transaction.is_debit())
        self.assertFalse(credit_transaction.is_debit())

    def test_is_credit(self):
        today = datetime.today()
        debit_transaction = Transaction(1, today, -100)
        credit_transaction = Transaction(2, today, 100)
        self.assertTrue(credit_transaction.is_credit())
        self.assertFalse(debit_transaction.is_credit())
