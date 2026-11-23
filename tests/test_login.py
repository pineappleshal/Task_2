import allure
import pytest

from data import INVALID_CREDENTIALS, make_user


@allure.feature('Вход пользователя')
class TestLogin:
    @allure.title('Вход с верными учётными данными')
    def test_login_existing_user(self, api, registered_user):
        response = api.login({key: registered_user[key] for key in ('email', 'password')})
        body = response.json()
        assert response.status_code == 200
        assert body['success'] is True
        assert body['user'] == {key: registered_user[key] for key in ('email', 'name')}
        assert body['accessToken'].startswith('Bearer ')
        assert isinstance(body['refreshToken'], str) and body['refreshToken']

    @allure.title('Вход с неверными данными: {fields}')
    @pytest.mark.parametrize('fields', [('email',), ('password',), ('email', 'password')],
                             ids=['wrong-email', 'wrong-password', 'both-wrong'])
    def test_login_invalid_credentials(self, api, registered_user, fields):
        payload = {key: registered_user[key] for key in ('email', 'password')}
        other = make_user()
        payload.update({field: other[field] for field in fields})
        response = api.login(payload)
        assert response.status_code == 401
        assert response.json() == INVALID_CREDENTIALS
