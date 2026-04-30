"""Factory for User test data."""

import factory

from app.models.user import User, UserRole
from app.utils.security import hash_password


class UserFactory(factory.Factory):
    class Meta:
        model = User

    store_id = 1
    username = factory.Sequence(lambda n: f"admin{n}")
    password_hash = factory.LazyFunction(lambda: hash_password("testpass"))
    role = UserRole.STORE_ADMIN
    is_active = True
    login_attempts = 0
