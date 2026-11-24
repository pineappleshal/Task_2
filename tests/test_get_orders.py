import allure

from data import UNAUTHORIZED


@allure.feature('Заказы пользователя')
class TestGetOrders:
    @allure.title('Авторизованный пользователь получает только свои заказы')
    def test_get_own_orders(self, authorized_api, own_order, another_users_order, ingredient_ids):
        response = authorized_api.orders()
        body = response.json()
        assert response.status_code == 200
        assert body['success'] is True
        assert isinstance(body['orders'], list)
        assert [order['number'] for order in body['orders']] == [own_order['number']]
        assert body['orders'][0]['ingredients'] == ingredient_ids
        assert another_users_order['number'] not in [order['number'] for order in body['orders']]

    @allure.title('Получение заказов без авторизации')
    def test_get_orders_unauthorized(self, api):
        response = api.orders()
        assert response.status_code == 401
        assert response.json() == UNAUTHORIZED
