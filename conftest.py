import allure
import pytest
import requests

from data import TU
from helper import UserMethods
from urls import URL

@pytest.fixture
def data_user():
    return TU.User_1


@pytest.fixture
def data_second_user():
    return TU.User_5



@allure.step('метод создает рандомного пользователя и удаляет его после теста')
@pytest.fixture
def create_and_delete_user():
    usermethods = UserMethods()
    created_data = usermethods.create_user()
    data = {
        "response": created_data["response"],
        "email": created_data["email"],
        "password": created_data["password"]
    }
    yield data
    token = created_data["response"].json().get("accessToken")
    usermethods.delete_user(token)



@allure.step('метод создает пользователя c заданными данными и удаляет его после теста')
@pytest.fixture
def create_and_delete_user_with_data(request):
    user_data = request.getfixturevalue("data_user")
    usermethods = UserMethods()
    # создание пользователя
    created_data = usermethods.create_user(
        email=user_data["email"],
        password=user_data["password"],
        name=user_data["name"]
    )

    yield created_data

    # удаление пользователя после завершения теста
    token = created_data["response"].json().get("accessToken")
    usermethods.delete_user(token)



@allure.step('метод создает второго пользователя c заданными данными и удаляет его после теста')
@pytest.fixture
def create_and_delete_second_user_with_data(request):
    user_data = request.getfixturevalue("data_second_user")
    usermethods = UserMethods()
    # создание пользователя
    created_data = usermethods.create_user(
        email=user_data["email"],
        password=user_data["password"],
        name=user_data["name"]
    )

    yield created_data

    # удаление пользователя после завершения теста
    token = created_data["response"].json().get("accessToken")
    usermethods.delete_user(token)



@allure.step('метод логинит пользователя c заданными данными и удаляет после теста')
@pytest.fixture
def register_login_delete_user_with_data(request):
    # получить данные из параметризации
    if hasattr(request, 'param'):
        user_data = request.param
    else:
        user_data = request.getfixturevalue("data_user")

    usermethods = UserMethods()
    # создать пользователя
    usermethods.create_user(
        email=user_data["email"],
        password=user_data["password"],
        name=user_data["name"]
    )
    # логин пользователя
    login_response = requests.post(
        URL.LOGIN_USER,
        json={
            "email": user_data["email"],
            "password": user_data["password"]
        }
    )
    yield {
        "response": login_response,
        "user_data": user_data,
        "token": login_response.json()["accessToken"]
    }
    # удалить пользователя
    usermethods.delete_user(login_response.json()["accessToken"])


# фикстура для создания заказа
@pytest.fixture
def create_order(request):
    ingredients = request.param
    create_order_response = requests.post(
        URL.CREATE_ORDER,
        json=ingredients
    )
    return create_order_response
