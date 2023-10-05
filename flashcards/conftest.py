import copy

import pytest
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
    return new_client


@pytest.fixture(scope="module")
def chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
