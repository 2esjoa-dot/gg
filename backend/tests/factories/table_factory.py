"""Factory for Table test data."""

import factory

from app.models.table import Table
from app.utils.security import hash_password


class TableFactory(factory.Factory):
    class Meta:
        model = Table

    store_id = 1
    table_number = factory.Sequence(lambda n: n + 1)
    password_hash = factory.LazyFunction(lambda: hash_password("tablepass"))
    is_active = True
