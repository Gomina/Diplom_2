import pytest
import allure

from data import TO
from helper import RequestsTools


class TestCreateOrder:

    @allure.title('Тест на успешное создание заказа с ингредиентами без авторизации')
    @pytest.mark.parametrize("ingredients", [[TO.ID_BUN_FLUORESCENT, TO.ID_BEEF_METEORITE, TO.ID_SPACE_SAUCE]])
    def test_create_order_with_ingredients_without_login(self, ingredients):
        # создать заказ:
        response = RequestsTools.requests_create_order_without_authorization(ingredients)
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
        response = RequestsTools.requests_create_order_without_authorization(ingredients)
        # проверка статус кода
        assert response.status_code == 400
        # проверка тела ответа
        response_json = response.json()
        assert response_json.get("message") ==  TO.BODY_ANSWER_NO_INGREDIENTS


    @allure.title('Тест на не успешное создание заказа с несуществующим ID ингредиента без авторизации')
    @pytest.mark.parametrize("ingredients", [[TO.ID_NON_EXISTENT_INGREDIENT]])
    def test_create_order_non_existent_ingredients_without_login(self, ingredients):
        # создать заказ:
        response = RequestsTools.requests_create_order_without_authorization(ingredients)
        # выводим тело ответа (HTML-формат)
        response_text = response.text
        # проверка статус кода
        assert response.status_code == 500
        assert "<title>Error</title>" in response_text


    @allure.title('Тест на успешное создание заказа с ингредиентами с авторизацией')
    @pytest.mark.parametrize("ingredients", [[TO.ID_BUN_FLUORESCENT, TO.ID_BEEF_METEORITE, TO.ID_SPACE_SAUCE]])
    def test_create_order_with_ingredients_user_authorized(self, create_and_delete_user, ingredients):
        # получить данные пользователя из фикстуры
        create_and_delete_user["user_data"]
        # авторизуем пользователя
        login_response = RequestsTools.requests_login_user(create_and_delete_user)
        token = login_response.json().get("accessToken")
        # создать заказ:
        response = RequestsTools.requests_create_order_authorized(ingredients, token)
        # проверка статус кода
        assert response.status_code == 200
        # проверка тела ответа
        response_json = response.json()
        expected_keys = ['name', 'order', 'success']
        assert set(expected_keys).issubset(response_json.keys())


    @allure.title('Тест на не успешное создание заказа без ингредиентом c авторизацией')
    @pytest.mark.parametrize("ingredients",[[]])
    def test_create_order_without_ingredients_user_authorized(self, create_and_delete_user, ingredients):
        # получить данные пользователя из фикстуры
        create_and_delete_user["user_data"]
        # авторизуем пользователя
        login_response = RequestsTools.requests_login_user(create_and_delete_user)
        token = login_response.json().get("accessToken")
        # создать заказ:
        response = RequestsTools.requests_create_order_authorized(ingredients, token)
        # проверка статус кода
        assert response.status_code == 400
        # проверка тела ответа
        response_json = response.json()
        assert response_json.get("message") == TO.BODY_ANSWER_NO_INGREDIENTS


    @allure.title('Тест на не успешное создание заказа с несуществующим ID ингредиента c авторизацией')
    @pytest.mark.parametrize("ingredients", [[TO.ID_NON_EXISTENT_INGREDIENT]])
    def test_create_order_non_existent_ingredients_user_authorized(self, create_and_delete_user, ingredients):
        # получить данные пользователя из фикстуры
        create_and_delete_user["user_data"]
        # авторизуем пользователя
        login_response = RequestsTools.requests_login_user(create_and_delete_user)
        token = login_response.json().get("accessToken")
        # создать заказ:
        response = RequestsTools.requests_create_order_authorized(ingredients, token)
        # вывести тело ответа (HTML-формат)
        response_text = response.text
        # проверка статус кода
        assert response.status_code == 500
        assert "<title>Error</title>" in response_text


class TestReceivingOrders:

    @allure.title('Тест на получение заказов авторизованного пользователя')
    @pytest.mark.parametrize("ingredients", [[TO.ID_BUN_FLUORESCENT, TO.ID_BEEF_METEORITE, TO.ID_SPACE_SAUCE]])
    def test_orders_login_user(self, create_and_delete_user, ingredients):
        # получить данные пользователя из фикстуры
        create_and_delete_user["user_data"]
        # авторизовать пользователя
        login_response = RequestsTools.requests_login_user(create_and_delete_user)
        token = login_response.json().get("accessToken")
        # создать заказ:
        RequestsTools.requests_create_order_authorized(ingredients, token)
        # запросить список заказов пользователя
        request_orders_response = RequestsTools.requests_get_user_orders(token)
        # проверка статуса ответа
        assert request_orders_response.status_code == 200
        # проверка тела ответа
        response_json = request_orders_response.json()
        expected_keys = {'success', 'orders', 'total', 'totalToday'}
        assert expected_keys.issubset(response_json.keys())


    @allure.title('Тест на неуспешное получение заказов не авторизованного пользователя')
    @pytest.mark.parametrize("ingredients", [[TO.ID_BUN_FLUORESCENT]])
    def test_orders_without_login_user(self, ingredients):
        # создать заказ
        RequestsTools.requests_create_order_without_authorization
        # запросить список заказов пользователя без авторизации
        request_orders_response = RequestsTools.requests_get_user_orders_without_authorization()
        # проверка статуса ответа
        assert request_orders_response.status_code == 401
        # проверка тела ответа
        response_json = request_orders_response.json()
        assert response_json.get("message") == TO.BODY_ANSWER_REQUESTING_USER_ORDERS_WITHOUT_AUTHORIZATION