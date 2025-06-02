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
    def create_user(self, email=None, password=None, name=None, allow_partial=False):
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

        response = requests.post(URL.CREATE_USER, json=payload)

        return {
            "email": payload.get("email"),
            "password": payload.get("password"),
            "name": payload.get("name"),
            "response": response
        }

    @allure.step('удалить пользователя')
    def delete_user(self, token):
        clean_token = token.replace("Bearer ", "") if token else token

        headers = {
            "Authorization": f"Bearer {clean_token}",  # Добавляем Bearer здесь
            "Content-Type": "application/json"
        }
        response = requests.delete(URL.DELETE_USER, headers=headers)
        return response