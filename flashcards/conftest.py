import copy

import pytest

from flashcards.models import User
from flashcards.tests.factories import UserFactory


@pytest.fixture(scope="function")
def user(db) -> User:
    return UserFactory()


@pytest.fixture(scope="function")
def authenticated_client(user, client):
    new_client = copy.deepcopy(client)
    new_client.force_login(user)
    return new_client
