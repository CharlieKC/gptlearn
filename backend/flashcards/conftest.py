import copy

import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import Client
from selenium import webdriver

from flashcards.models import User
from flashcards.tests.factories import UserFactory


@pytest.fixture(scope="function")
def user(db) -> User:
    return UserFactory()


@pytest.fixture(scope="function")
def authenticated_client(user, client):
    new_client = copy.deepcopy(client)
    new_client.force_login(user)
    new_client.user = user
    return new_client


@pytest.fixture(scope="function")
def client_factory():
    def get(auth=True):
        client = Client()
        if auth:
            user = UserFactory()
            client.force_login(user)
            client.user = user
        else:
            client.user = AnonymousUser()
        return client

    return get


@pytest.fixture(scope="module")
def chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
