from model.account import Account
from serializers.transaction_serializer import TransactionSerializer


class AccountSerializer:
    def serialize(self, account):
        return {
            'id': account.id,
            'description': account.description,
            'transactions': TransactionSerializer().serialize_all(account.transactions()),
        }

    def deserialize(self, data):
        transactions = {transaction.id: transaction for transaction in
                        TransactionSerializer().deserialize_all(data['transactions'])}
        return Account(data['id'], data['description'], transactions)
