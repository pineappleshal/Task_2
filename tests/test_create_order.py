import allure
import pytest

from data import NO_INGREDIENTS, UNAUTHORIZED


@allure.feature('Создание заказа')
class TestCreateOrder:
    @allure.title('Создание заказа с авторизацией и ингредиентами')
    def test_create_order_authorized(self, authorized_api, ingredient_ids):
        response = authorized_api.create_order({'ingredients': ingredient_ids})
        body = response.json()
        assert response.status_code == 200
        assert body['success'] is True
        assert isinstance(body['order']['number'], int) and body['order']['number'] > 0
        assert [item['_id'] for item in body['order']['ingredients']] == ingredient_ids

    @allure.title('Создание заказа без авторизации')
    def test_create_order_without_authorization(self, api, ingredient_ids):
        response = api.create_order({'ingredients': ingredient_ids})
        assert response.status_code == 401
        assert response.json() == UNAUTHORIZED

    @allure.title('Создание заказа без ингредиентов: {payload}')
    @pytest.mark.parametrize('payload', [{}, {'ingredients': []}], ids=['missing', 'empty'])
    def test_create_order_without_ingredients(self, authorized_api, payload):
        response = authorized_api.create_order(payload)
        assert response.status_code == 400
        assert response.json() == NO_INGREDIENTS

    @allure.title('Создание заказа с некорректным хешем ингредиента')
    def test_create_order_invalid_ingredient_hash(self, authorized_api):
        response = authorized_api.create_order({'ingredients': ['ffffffffffffffffffffffff']})
        assert response.status_code == 500
        # Формат тела ошибки 500 в документации не задан.
        assert response.text.strip()
