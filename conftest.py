import allure
import pytest
import requests

from data import TU
from helper import UserMethods
from urls import URL


@allure.step('метод удаляет пользователя после теста')
@pytest.fixture
def delete_created_user():
    tokens_to_delete = []  # собрать токен для удаления
    def add_token(token):
        tokens_to_delete.append(token)
    yield add_token
    # после завершения теста удаляем пользователя
    usermethods = UserMethods()
    for token in tokens_to_delete:
        usermethods.delete_user(token)


@allure.step('метод создает пользователя и удаляет его после теста')
@pytest.fixture
def create_and_delete_user():
    usermethods = UserMethods()
    # создать пользователя
    create_response = requests.post(URL.CREATE_USER, json=TU.User_1)
    # вернуть данные пользователя
    yield {
        "response": create_response,
        "user_data": TU.User_1,
        "token": create_response.json().get("accessToken")
    }

    # удалить пользователя после завершения теста
    usermethods.delete_user(create_response.json().get("accessToken"))


@allure.step('метод создает вторго пользователя (из TU.User_5) и удаляет его после теста')
@pytest.fixture
def create_and_delete_second_user():
    usermethods = UserMethods()
    # создать пользователя
    create_response = requests.post(URL.CREATE_USER, json=TU.User_5)
    # вернуть данные пользователя
    yield {
        "response": create_response,
        "user_data": TU.User_1,
        "token": create_response.json().get("accessToken")
    }

    # удалить пользователя после завершения теста
    usermethods.delete_user(create_response.json().get("accessToken"))