import allure
import pytest

from data import REQUIRED_FIELDS, USER_EXISTS


@allure.feature('Создание пользователя')
class TestCreateUser:
    @allure.title('Создание уникального пользователя')
    def test_create_unique_user(self, user_factory, user_data):
        response = user_factory(user_data)
        body = response.json()
        assert response.status_code == 200
        assert body['success'] is True
        assert body['user'] == {'email': user_data['email'], 'name': user_data['name']}
        assert body['accessToken'].startswith('Bearer ')
        assert isinstance(body['refreshToken'], str) and body['refreshToken']

    @allure.title('Повторная регистрация пользователя')
    def test_create_existing_user(self, registered_user, user_factory, user_data):
        response = user_factory(user_data)
        assert response.status_code == 403
        assert response.json() == USER_EXISTS

    @allure.title('Регистрация без обязательного поля: {field}')
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_create_without_required_field(self, user_factory, user_data, field):
        user_data.pop(field)
        response = user_factory(user_data)
        assert response.status_code == 403
        assert response.json() == REQUIRED_FIELDS
