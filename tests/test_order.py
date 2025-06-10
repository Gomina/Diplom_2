import pytest
import allure
import requests

from data import TO
from urls import URL


class TestCreateOrder:

    @allure.title('Тест на успешное создание заказа с ингредиентами без авторизации')
    @pytest.mark.parametrize("ingredients", [[TO.ID_BUN_FLUORESCENT, TO.ID_BEEF_METEORITE, TO.ID_SPACE_SAUCE]])
    def test_create_order_with_ingredients_without_login(self, ingredients):
        # создать заказ:
        response = requests.post(URL.CREATE_ORDER, json={"ingredients": ingredients})
        # проверка статус кода
        assert response.status_code == 200
        # проверка тела ответа
        response_json = response.json()
        expected_keys = ['name', 'order', 'success']
        assert set(expected_keys).issubset(response_json.keys())


    @allure.title('Тест на не успешное создание заказа без ингредиентом без авторизации')
    @pytest.mark.parametrize("ingredients",[[]])
    def test_create_order_without_ingredients_without_login(self, ingredients):
        # создать заказ:
        response = requests.post(URL.CREATE_ORDER, json={"ingredients": ingredients})
        # проверка статус кода
        assert response.status_code == 400
        # проверка тела ответа
        response_json = response.json()
        assert response_json.get("message") ==  TO.BODY_ANSWER_NO_INGREDIENTS


    @allure.title('Тест на не успешное создание заказа с несуществующим ID ингредиента без авторизации')
    @pytest.mark.parametrize("ingredients", [[TO.ID_NON_EXISTENT_INGREDIENT]])
    def test_create_order_non_existent_ingredients_without_login(self, ingredients):
        # создать заказ:
        response = requests.post(URL.CREATE_ORDER, json={"ingredients": ingredients})
        # выводим тело ответа (HTML-формат)
        response_text = response.text
        # проверка статус кода
        assert response.status_code == 500
        assert "<title>Error</title>" in response_text


    @allure.title('Тест на успешное создание заказа с ингредиентами с авторизацией')
    @pytest.mark.parametrize("ingredients", [[TO.ID_BUN_FLUORESCENT, TO.ID_BEEF_METEORITE, TO.ID_SPACE_SAUCE]])
    def test_create_order_with_ingredients_user_authorized(self, register_login_delete_user_with_data, ingredients):
        # залогинить пользователя
        register_login_delete_user_with_data
        # создать заказ:
        response = requests.post(URL.CREATE_ORDER, json={"ingredients": ingredients})
        # проверка статус кода
        assert response.status_code == 200
        # проверка тела ответа
        response_json = response.json()
        expected_keys = ['name', 'order', 'success']
        assert set(expected_keys).issubset(response_json.keys())


    @allure.title('Тест на не успешное создание заказа без ингредиентом c авторизацией')
    @pytest.mark.parametrize("ingredients",[[]])
    def test_create_order_without_ingredients_user_authorized(self, register_login_delete_user_with_data, ingredients):
        # залогинить пользователя
        register_login_delete_user_with_data
        # создать заказ:
        response = requests.post(URL.CREATE_ORDER, json={"ingredients": ingredients})
        # проверка статус кода
        assert response.status_code == 400
        # проверка тела ответа
        response_json = response.json()
        assert response_json.get("message") == TO.BODY_ANSWER_NO_INGREDIENTS


    @allure.title('Тест на не успешное создание заказа с несуществующим ID ингредиента c авторизацией')
    @pytest.mark.parametrize("ingredients", [[TO.ID_NON_EXISTENT_INGREDIENT]])
    def test_create_order_non_existent_ingredients_user_authorized(self, register_login_delete_user_with_data, ingredients):
        # залогинить пользователя
        register_login_delete_user_with_data
        # создать заказ:
        response = requests.post(URL.CREATE_ORDER, json={"ingredients": ingredients})
        # вывести тело ответа (HTML-формат)
        response_text = response.text
        # проверка статус кода
        assert response.status_code == 500
        assert "<title>Error</title>" in response_text


class TestReceivingOrders:


    @allure.title('Тест на получение заказов авторизованного пользователя')
    def test_orders_login_user(self, register_login_delete_user_with_data):
        # получить токен авторизации
        auth_token = register_login_delete_user_with_data['token']
        # создать заказ
        ingredient_id = TO.ID_BUN_FLUORESCENT
        order_response = requests.post(URL.CREATE_ORDER, json={'ingredients': [ingredient_id]}, headers={
            'Authorization': auth_token
        })
        # запросить список заказов пользователя
        headers = {"Authorization": auth_token}
        request_orders_response = requests.get(URL.RECEIVE_ORDER, headers=headers)
        # проверка статус кода
        assert order_response.status_code == 200
        # проверка тела ответа
        response_json = request_orders_response.json()
        expected_keys = {'success', 'orders', 'total', 'totalToday'}
        assert expected_keys.issubset(response_json.keys())


    @allure.title('Тест на получение заказов не авторизованного пользователя')
    @pytest.mark.parametrize("ingredients", [[TO.ID_BUN_FLUORESCENT]])
    def test_orders_without_login_user(self, ingredients):
        # создать заказ
        requests.post(URL.CREATE_ORDER, json={"ingredients": ingredients})
        # запросить список заказов пользователя без авторизации
        request_orders_response = requests.get(URL.RECEIVE_ORDER)
        # проверка статус кода
        assert request_orders_response.status_code == 401
        # проверка тела ответа
        response_json = request_orders_response.json()
        assert response_json.get("message") == TO.BODY_ANSWER_REQUESTING_USER_ORDERS_WITHOUT_AUTHORIZATION