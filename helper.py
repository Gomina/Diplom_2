import token
import allure
import requests
import random
import string
import pytest

from urls import URL


class UserMethods:


    @staticmethod
    @allure.step('генерация случайной строки из букв нижнего регистра для логина или пароля')
    def generate_random_string(length=10):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


    @staticmethod
    @allure.step('генерация случайной почты')
    def generate_random_email(length=10):
        random_part = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
        return f"{random_part}@yandex.ru"


    @allure.step('создать нового пользователя')
    def create_user_payload(self, email=None, password=None, name=None, allow_partial=False):
        payload = {}

        # если все данные введены или все поля пустые
        if allow_partial or all(v is None for v in [email, password, name]):
            payload = {
                "email": email if email is not None else self.generate_random_email(),
                "password": password if password is not None else self.generate_random_string(),
                "name": name if name is not None else self.generate_random_string()
            }
        else:
            # если хоть одно поле заполнено
            if email is not None:
                payload["email"] = email
            if password is not None:
                payload["password"] = password
            if name is not None:
                payload["name"] = name

        return payload

    @allure.step('удалить пользователя')
    def delete_user(self, token):
        clean_token = token.replace("Bearer ", "") if token else token

        headers = {
            "Authorization": f"Bearer {clean_token}",  # Добавляем Bearer здесь
            "Content-Type": "application/json"
        }
        response = requests.delete(URL.DELETE_USER, headers=headers)
        return response


class RequestsTools:

    @staticmethod
    @allure.step('метода отправки запроса "Создание заказа" без авторизации')
    def requests_create_order_without_authorization(ingredients):
        response = requests.post(URL.CREATE_ORDER, json={"ingredients": ingredients})
        return response


    @staticmethod
    @allure.step('метода отправки запроса "Создание заказа" с авторизацией')
    def requests_create_order_authorized(ingredients, token):
        headers = {
            "Authorization": token
        }
        response = requests.post(URL.CREATE_ORDER, json={"ingredients": ingredients}, headers=headers)
        return response


    @staticmethod
    @allure.step('метода отправки запроса "Авторизация и регистрация"')
    def requests_login_user(create_and_delete_user):
        user_data = create_and_delete_user["user_data"]
        # авторизовать пользователя
        login_response = requests.post(
            URL.LOGIN_USER,
            json={
                "email": user_data["email"],
                "password": user_data["password"]
            }
        )
        return login_response

    @staticmethod
    @allure.step('метода отправки запроса "Авторизация пользователя"')
    def requests_login_user_incorrect_data(email, password):
        response = requests.post(
            URL.LOGIN_USER,
            json={
                "email": email,
                "password": password
            }
        )
        return response



    @staticmethod
    @allure.step('метода отправки запроса "Получить заказы конкретного пользователя" с авторизацией')
    def requests_get_user_orders(token):
        headers = {
            "Authorization": token
        }
        response = requests.get(URL.RECEIVE_ORDER, headers=headers)
        return response


    @staticmethod
    @allure.step('метода отправки запроса "Получить заказы пользователя" без авторизации"')
    def requests_get_user_orders_without_authorization():
        response = requests.get(URL.RECEIVE_ORDER)
        return response


    @staticmethod
    @allure.step('метода отправки запроса "Создание пользователя"')
    def requests_creation_user(payload):
        response = requests.post(URL.CREATE_USER, json=payload)
        return response

    @staticmethod
    @allure.step('метод отправки запроса "Получение и обновление информации о пользователе" с токином')
    def requests_update_user(new_data, token):
        headers = {
            "Authorization": token
        }
        response = requests.patch(URL.CHANGE_USER, json=new_data, headers=headers)
        return response


    @staticmethod
    @allure.step('метод отправки запроса "Получение и обновление информации о пользователе" без токена')
    def requests_update_user_without_token(new_data):
        response = requests.patch(URL.CHANGE_USER, json=new_data)
        return response