import json

from redis.client import Redis

from serializers.account_serializer import AccountSerializer


class AccountManager:
    def __init__(self, redis=None):
        self.serializer = AccountSerializer()
        if redis is None:
            self.redis = Redis(host='localhost', port=6379, db=0)  # This should be in a conf file
        else:
            self.redis = redis

    def save(self, account):
        self.redis.set(
            self._key_for(account.id),
            json.dumps(self.serializer.serialize(account))
        )

    def get(self, account_id):
        data = self.redis.get(self._key_for(account_id))
        if data:
            return self.serializer.deserialize(json.loads(data))

    def delete(self, account):
        self.redis.delete(self._key_for(account.id))

    def _key_for(self, account_id):
        return f'account-{account_id}'
