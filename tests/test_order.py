import pytest
import allure
import requests

from data import TO
from urls import URL


class TestCreateOrder:

    @allure.title('Тест на успешное создание заказа с ингредиентами без авторизации')
    @pytest.mark.parametrize("create_order", [
        {"ingredients": [TO.ID_BUN_FLUORESCENT, TO.ID_BEEF_METEORITE, TO.ID_SPACE_SAUCE]}],
        indirect=True
    )
    def test_create_order_with_ingredients_without_login(self, create_order):
        # проверка статус кода
        assert create_order.status_code == 200
        # проверка тела ответа
        response_json = create_order.json()
        expected_keys = ['name', 'order', 'success']
        assert set(expected_keys).issubset(response_json.keys())


    @allure.title('Тест на не успешное создание заказа без ингредиентом без авторизации')
    @pytest.mark.parametrize("create_order", [
        {"ingredients": []}], indirect=True
    )
    def test_create_order_without_ingredients_without_login(self, create_order):
        # проверка статус кода
        assert create_order.status_code == 400
        # проверка тела ответа
        response_json = create_order.json()
        assert response_json.get("message") ==  TO.BODY_ANSWER_NO_INGREDIENTS


    @allure.title('Тест на не успешное создание заказа с несуществующим ID ингредиента без авторизации')
    @pytest.mark.parametrize("create_order", [
        {"ingredients": [TO.ID_NON_EXISTENT_INGREDIENT]}],
        indirect=True
    )
    def test_create_order_non_existent_ingredients_without_login(self, create_order):
        # выводим тело ответа (HTML-формат)
        response_text = create_order.text
        # проверка статус кода
        assert create_order.status_code == 500
        assert "<title>Error</title>" in response_text


    @allure.title('Тест на успешное создание заказа с ингредиентами с авторизацией')
    @pytest.mark.parametrize("create_order", [
        {"ingredients": [TO.ID_BUN_FLUORESCENT, TO.ID_BEEF_METEORITE, TO.ID_SPACE_SAUCE]}],
        indirect=True
    )
    def test_create_order_with_ingredients_user_authorized(self, register_login_delete_user_with_data, create_order):
        # залогинить пользователя
        register_login_delete_user_with_data
        # проверка статус кода
        assert create_order.status_code == 200
        # проверка тела ответа
        response_json = create_order.json()
        expected_keys = ['name', 'order', 'success']
        assert set(expected_keys).issubset(response_json.keys())


    @allure.title('Тест на не успешное создание заказа без ингредиентом c авторизацией')
    @pytest.mark.parametrize("create_order", [
        {"ingredients": []}], indirect=True
    )
    def test_create_order_without_ingredients_user_authorized(self, register_login_delete_user_with_data, create_order):
        # залогинить пользователя
        register_login_delete_user_with_data
        # проверка статус кода
        assert create_order.status_code == 400
        # проверка тела ответа
        response_json = create_order.json()
        assert response_json.get("message") == TO.BODY_ANSWER_NO_INGREDIENTS


    @allure.title('Тест на не успешное создание заказа с несуществующим ID ингредиента c авторизацией')
    @pytest.mark.parametrize("create_order", [
        {"ingredients": [TO.ID_NON_EXISTENT_INGREDIENT]}],
        indirect=True
    )
    def test_create_order_non_existent_ingredients_user_authorized(self, register_login_delete_user_with_data, create_order):
        # залогинить пользователя
        register_login_delete_user_with_data
        # вывести тело ответа (HTML-формат)
        response_text = create_order.text
        # проверка статус кода
        assert create_order.status_code == 500
        assert "<title>Error</title>" in response_text


class TestReceivingOrders:


    @allure.title('Тест на получение заказов авторизованного пользователя')
    @pytest.mark.parametrize("create_order", [
        {"ingredients": [TO.ID_BUN_FLUORESCENT]}],
        indirect=True
    )
    def test_orders_login_user(self, register_login_delete_user_with_data, create_order):
        # залогинить пользователя
        register_login_delete_user_with_data
        # создать заказ
        create_order
        # получить токен авторизации
        auth_token = register_login_delete_user_with_data['token']
        # запросить список заказов пользователя
        headers = {"Authorization": auth_token}
        request_orders_response = requests.get(URL.RECEIVE_ORDER, headers=headers)
        # проверка статус кода
        assert request_orders_response.status_code == 200
        # проверка тела ответа
        response_json = request_orders_response.json()
        expected_keys = ['success', 'orders', 'total', 'totalToday']
        assert set(expected_keys).issubset(response_json.keys())


    @allure.title('Тест на получение заказов не авторизованного пользователя')
    @pytest.mark.parametrize("create_order", [
        {"ingredients": [TO.ID_BUN_FLUORESCENT]}],
        indirect=True
    )
    def test_orders_without_login_user(self, create_order):
        # создать заказ
        create_order
        # запросить список заказов пользователя без авторизации
        request_orders_response = requests.get(URL.RECEIVE_ORDER)
        # проверка статус кода
        assert request_orders_response.status_code == 401
        # проверка тела ответа
        response_json = request_orders_response.json()
        assert response_json.get("message") == TO.BODY_ANSWER_REQUESTING_USER_ORDERS_WITHOUT_AUTHORIZATION