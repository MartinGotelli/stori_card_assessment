import unittest
from datetime import date

from model.account import Account
from model.transaction import Transaction


class AccountTests(unittest.TestCase):
    def setUp(self):
        self.transaction = Transaction(1, date.today(), 100)

    def test_creation(self):
        account_id = 87
        description = 'Stori Account'
        transactions = {self.transaction.id: self.transaction}
        account = Account(account_id, description, transactions)
        self.assertEqual(account.id, account_id)
        self.assertEqual(account.description, description)
        self.assertEqual(account.transactions_by_id, transactions)

    def test_creation_transactions_is_optional(self):
        account_id = 87
        description = 'Stori Account'
        account = Account(account_id, description)
        self.assertEqual(account.id, account_id)
        self.assertEqual(account.description, description)
        self.assertEqual(account.transactions_by_id, {})

    def test_transactions(self):
        account = Account(87, 'Test Account', {1: self.transaction})
        self.assertEqual(account.transactions(), [self.transaction])

    def test_add_transaction(self):
        account = Account(1, 'Test Account')
        self.assertEqual(account.transactions_by_id, {})
        account.add_transaction(self.transaction)
        self.assertEqual(account.transactions_by_id[self.transaction.id], self.transaction)

    def test_transactions_from_month(self):
        november_transaction = Transaction(1, date(2022, 11, 10), 100)
        february_transaction = Transaction(2, date(2022, 2, 10), 100)
        account = Account(87, 'Test Account', {1: november_transaction, 2: february_transaction})
        self.assertListEqual(list(account.transactions_on(2)), [february_transaction])
        self.assertListEqual(list(account.transactions_on(11)), [november_transaction])
        self.assertListEqual(list(account.transactions_on(5)), [])

    def test_debit_transactions_on(self):
        november_credit = Transaction(1, date(2022, 11, 10), 100)
        november_debit = Transaction(2, date(2022, 11, 10), -100)
        february_credit = Transaction(3, date(2022, 2, 10), 100)
        account = Account(87, 'Test Account', {1: november_credit, 2: november_debit, 3: february_credit})
        self.assertListEqual(account.debit_transactions_on(11), [november_debit])
        self.assertListEqual(account.debit_transactions_on(2), [])
        self.assertListEqual(account.debit_transactions_on(5), [])

    def test_credit_transactions_on(self):
        november_credit = Transaction(1, date(2022, 11, 10), 100)
        november_debit = Transaction(2, date(2022, 11, 10), -100)
        february_credit = Transaction(3, date(2022, 2, 10), 100)
        account = Account(87, 'Test Account', {1: november_credit, 2: november_debit, 3: february_credit})
        self.assertListEqual(account.credit_transactions_on(11), [november_credit])
        self.assertListEqual(account.credit_transactions_on(2), [february_credit])
        self.assertListEqual(account.credit_transactions_on(5), [])

    def test_average_debit_on(self):
        november_credit = Transaction(1, date(2022, 11, 10), 100)
        november_debit_100 = Transaction(2, date(2022, 11, 10), -100)
        november_debit_21 = Transaction(3, date(2022, 11, 10), -21.55)
        february_debit = Transaction(4, date(2022, 2, 10), -100)
        account = Account(
            87,
            'Test Account',
            {1: november_credit, 2: november_debit_100, 3: november_debit_21, 4: february_debit}
        )
        self.assertEqual(account.average_debit_on(11), round((-100 - 21.55) / 2, 2))
        self.assertEqual(account.average_debit_on(2), -100)
        self.assertEqual(account.average_debit_on(5), 0)

    def test_average_credit_on(self):
        november_credit_100 = Transaction(1, date(2022, 11, 10), 100)
        november_debit = Transaction(2, date(2022, 11, 10), -100)
        november_credit_21 = Transaction(3, date(2022, 11, 10), 21.55)
        february_credit = Transaction(4, date(2022, 2, 10), 100)
        account = Account(
            87,
            'Test Account',
            {1: november_credit_100, 2: november_debit, 3: november_credit_21, 4: february_credit}
        )
        self.assertEqual(account.average_credit_on(11), round((100 + 21.55) / 2, 2))
        self.assertEqual(account.average_credit_on(2), 100)
        self.assertEqual(account.average_credit_on(5), 0)
