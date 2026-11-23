import allure
import pytest

from data import UNAUTHORIZED, make_user


@allure.feature('Изменение пользователя')
class TestUpdateUser:
    @allure.title('Изменение поля {field} с авторизацией')
    @pytest.mark.parametrize('field', ['email', 'name'])
    def test_update_profile_authorized(self, authorized_api, registered_user, field):
        value = make_user()['email'] if field == 'email' else 'Новое имя'
        response = authorized_api.update_user({field: value})
        expected = {key: registered_user[key] for key in ('email', 'name')}
        expected[field] = value
        assert response.status_code == 200
        assert response.json() == {'success': True, 'user': expected}

    @allure.title('Изменение пароля с авторизацией')
    def test_update_password_authorized(self, authorized_api, api, registered_user):
        password = make_user()['password']
        response = authorized_api.update_user({'password': password})
        login = api.login({'email': registered_user['email'], 'password': password})
        assert response.status_code == 200
        assert response.json() == {'success': True, 'user': {
            key: registered_user[key] for key in ('email', 'name')}}
        assert login.status_code == 200 and login.json()['success'] is True

    @allure.title('Изменение поля {field} без авторизации')
    @pytest.mark.parametrize('field', ['email', 'name', 'password'])
    def test_update_without_authorization(self, api, registered_user, field):
        value = 'Другое имя' if field == 'name' else make_user()[field]
        response = api.update_user({field: value})
        assert response.status_code == 401
        assert response.json() == UNAUTHORIZED
