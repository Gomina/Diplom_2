import pytest
import allure
import requests

from data import TU
from helper import UserMethods
from urls import URL


class TestUserCreation:



    @allure.title('Тест на успешное создание уникального пользователя')
    def test_creation_unique_user(self, create_and_delete_user):
        user_data = create_and_delete_user
        # проверка статус кода
        assert user_data["response"].status_code == 200
        # проверка тела ответа
        assert "accessToken" in user_data["response"].json()


    @allure.title('Тест на ошибку при создании пользователя, который уже создан')
    def test_re_creating_user(self, create_and_delete_user_with_data):
        create_and_delete_user_with_data
        usermethods = UserMethods()
        # попытка создать пользователя с такими же данными
        second_creation_attempt = usermethods.create_user(
            email=TU.User_1["email"],
            password=TU.User_1["password"],
            name=TU.User_1["name"]
        )
        # проверка статус кода
        assert second_creation_attempt["response"].status_code == 403
        # проверка тела ответа
        content =  second_creation_attempt["response"].json()
        assert content.get("message") == TU.BODY_ANSWER_USER_EXISTS


    @allure.title('Тест на ошибку при создании пользователя без одного из обязательных полей')
    @pytest.mark.parametrize('user_data', [
        pytest.param(TU.User_2, id='User_2'),
        pytest.param(TU.User_3, id='User_3'),
        pytest.param(TU.User_4, id='User_4')
    ])
    def test_creation_user_without_one_data(self, user_data):
        usermethods = UserMethods()
        # попытка создать пользователя
        response_data = usermethods.create_user(
            email=user_data["email"],
            password=user_data["password"],
            name=user_data["name"]
        )
        # проверка статус кода
        assert response_data["response"].status_code == 403
        # проверка тела ответа
        content = response_data['response'].json()
        assert content.get("message") == TU.BODY_ANSWER_ONE_FIELDS_NOT_FILLED_IN





class TestUserLogin:

    @allure.title('Тест успешной авторизации пользователя с заданными параметрами')
    def test_login_user_with_data(self, register_login_delete_user_with_data):
        test_data = register_login_delete_user_with_data
        response = test_data["response"]
        user_data = test_data["user_data"]
        # проверка статус-кода
        assert response.status_code == 200
        # проверка тела ответа
        response_json = response.json()
        assert all([
            response_json["success"] is True,
            "accessToken" in response_json,
            "refreshToken" in response_json,
            response_json["user"]["email"] == user_data["email"],
            response_json["user"]["name"] == user_data["name"]
        ])


    @allure.title('Тест неуспешной авторизации пользователя с неверными данными')
    @pytest.mark.parametrize("user_data_login", [TU.User_6, TU.User_7])
    def test_login_user_unfaithful_password(self, user_data_login, create_and_delete_user_with_data):
        # логин пользователя с неверным паролем
        login_response = requests.post(
            URL.LOGIN_USER,
            json={
                "email": user_data_login["email"],
                "password": user_data_login["password"]
            }
        )
        # проверка статус кода
        assert login_response.status_code == 401
        # проверка тела ответа
        response_json = login_response.json()
        assert response_json.get("message") == TU.BODY_ANSWER_AUTHORIZATION_FAILED



class TestUserСhange:

    @allure.title('Тест успешного изменения почты авторизованного пользователя')
    def test_change_email(self, register_login_delete_user_with_data):
        # получить данные авторизованного пользователя из фикстуры
        test_data = register_login_delete_user_with_data
        token = test_data["token"]
        original_user_data = test_data["user_data"]
        # новая почта для изменения (из TU.User_8)
        new_data = {
            "email": TU.User_8["email"],
            "name": original_user_data["name"],
            "password": original_user_data["password"]
        }
        # отправить запрос на изменение данных
        change_response = requests.patch(
            URL.CHANGE_USER,
            headers={"Authorization": token},
            json=new_data
        )
        # проверка статус кода
        assert change_response.status_code == 200
        # проверка тела ответа
        response_json = change_response.json()
        assert response_json == {
            "success": True,
            "user": {
                "email": TU.User_8["email"],
                "name": TU.User_1["name"]
            }
        }

    @allure.title('Тест успешного изменения имени авторизованного пользователя')
    def test_change_name(self, register_login_delete_user_with_data):
        # получить данные авторизованного пользователя из фикстуры
        test_data = register_login_delete_user_with_data
        token = test_data["token"]
        original_user_data = test_data["user_data"]
        # новое имя для изменения (из TU.User_8)
        new_data = {
            "email": original_user_data["email"],
            "name": TU.User_8["name"],
            "password": original_user_data["password"]
        }
        # отправить запрос на изменение данных
        change_response = requests.patch(
            URL.CHANGE_USER,
            headers={"Authorization": token},
            json=new_data
        )
        # проверка статус кода
        assert change_response.status_code == 200
        # проверка тела ответа
        response_json = change_response.json()
        assert response_json == {
            "success": True,
            "user": {
                "email": TU.User_1["email"],
                "name": TU.User_8["name"]
            }
        }


    @allure.title('Тест успешного изменения пароля авторизованного пользователя')
    def test_change_password(self, register_login_delete_user_with_data):
        # получить данные авторизованного пользователя из фикстуры
        test_data = register_login_delete_user_with_data
        token = test_data["token"]
        original_user_data = test_data["user_data"]
        # новый пароль для изменения (из TU.User_8)
        new_data = {
            "email": original_user_data["email"],
            "name": original_user_data["name"],
            "password": TU.User_8["password"]
        }
        # отправить запрос на изменение данных
        change_response = requests.patch(
            URL.CHANGE_USER,
            headers={"Authorization": token},
            json=new_data
        )
        # проверка статус кода
        assert change_response.status_code == 200
        # проверка тела ответа
        response_json = change_response.json()
        assert response_json == {
            "success": True,
            "user": {
                "email": TU.User_1["email"],
                "name": TU.User_1["name"]
            }
        }


    @allure.title('Тест на успешное изменение всех данных авторизованного пользователя')
    def test_change_all_data(self, register_login_delete_user_with_data):
        # получить данные авторизованного пользователя из фикстуры
        test_data = register_login_delete_user_with_data
        token = test_data["token"]
        test_data["user_data"]
        # новый пароль для изменения (из TU.User_8)
        new_data = {
            "email": TU.User_8["email"],
            "name": TU.User_8["name"],
            "password": TU.User_8["password"]
        }
        # отправить запрос на изменение данных
        change_response = requests.patch(
            URL.CHANGE_USER,
            headers={"Authorization": token},
            json=new_data
        )
        # проверка статус кода
        assert change_response.status_code == 200
        # проверка тела ответа
        response_json = change_response.json()
        assert response_json == {
            "success": True,
            "user": {
                "email": TU.User_8["email"],
                "name": TU.User_8["name"]
            }
        }


    @allure.title('Тест на неуспешное изменение данных авторизованного, но не залогиненного пользователя')
    def test_inability_change_all_data_without_login(self, create_and_delete_user_with_data):
        # получить данные авторизованного пользователя из фикстуры
        create_and_delete_user_with_data
        # новые данные для изменения (из TU.User_8)
        new_data = {
            "email": TU.User_8["email"],
            "name": TU.User_8["name"],
            "password": TU.User_8["password"]
        }
        # отправить запрос на изменение данных БЕЗ токена
        change_response = requests.patch(
            URL.CHANGE_USER,
            headers={},  # без заголовка авторизации
            json=new_data
        )
        # проверка статус кода
        assert change_response.status_code == 401
        # проверка тела ответа
        response_json = change_response.json()
        assert response_json.get("message") == TU.BODY_ANSWER_YOU_MUST_BE_LOGGED_IN


    @allure.title('Тест на неуспешное изменение почты авторизованного пользователя, если такая почта уже есть у другого пользователя')
    def test_inability_change_email_owned_another_user(self, register_login_delete_user_with_data, create_and_delete_second_user_with_data):
        # получить данные авторизованного пользователя 1
        test_data = register_login_delete_user_with_data
        token = test_data["token"]
        original_user_data = test_data["user_data"]
        # создать второго пользователя
        create_and_delete_second_user_with_data
        # новые данные для изменения 1 пользователя (из TU.User_5)
        new_data = {
            "email": TU.User_5["email"],
            "name": original_user_data["name"],
            "password": original_user_data["password"]
        }
        # отправить запрос на изменение данных БЕЗ токена
        change_response = requests.patch(
            URL.CHANGE_USER,
            headers={"Authorization": token},
            json=new_data
        )
        # проверка статус кода
        assert change_response.status_code == 403
        # проверка тела ответа
        response_json = change_response.json()
        assert response_json.get("message") == TU.BODY_ANSWER_ANOTHER_USER_ALREADY_HAS_THIS_EMAIL



