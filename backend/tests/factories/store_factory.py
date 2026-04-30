"""Factory for Store test data."""

import factory

from app.models.store import Store


class StoreFactory(factory.Factory):
    class Meta:
        model = Store

    name = factory.Sequence(lambda n: f"Test Store {n}")
    code = factory.Sequence(lambda n: f"test-store-{n}")
    address = factory.Faker("address")
    is_active = True
