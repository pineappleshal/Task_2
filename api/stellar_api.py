import json

import allure
import requests

from config import BASE_URL, TIMEOUT


def redact(value):
    if isinstance(value, dict):
        return {key: '<hidden>' if key.lower() in
                {'password', 'accesstoken', 'refreshtoken', 'authorization'}
                else redact(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact(item) for item in value]
    return value


class StellarApi:
    def __init__(self, token=None):
        self.session = requests.Session()
        self.token = token

    def close(self):
        self.session.close()

    def request(self, method, path, payload=None):
        headers = {'Authorization': self.token} if self.token else {}
        with allure.step(f'{method} {path}'):
            allure.attach(json.dumps(redact(payload), ensure_ascii=False),
                          'Тело запроса', allure.attachment_type.JSON)
            response = self.session.request(method, BASE_URL + '/api' + path,
                                            json=payload, headers=headers, timeout=TIMEOUT)
            try:
                body = json.dumps(redact(response.json()), ensure_ascii=False)
            except requests.exceptions.JSONDecodeError:
                body = response.text
            allure.attach(f'HTTP {response.status_code}\n{body}',
                          'Ответ сервера', allure.attachment_type.TEXT)
            return response

    # Контекстный шаг не сохраняет пароль в параметрах Allure-декоратора.
    def register(self, payload):
        with allure.step('Создать пользователя'):
            return self.request('POST', '/auth/register', payload)

    def login(self, payload):
        with allure.step('Войти в аккаунт'):
            return self.request('POST', '/auth/login', payload)

    def update_user(self, payload):
        with allure.step('Изменить данные пользователя'):
            return self.request('PATCH', '/auth/user', payload)

    @allure.step('Удалить тестового пользователя')
    def delete_user(self):
        return self.request('DELETE', '/auth/user')

    @allure.step('Получить ингредиенты')
    def ingredients(self):
        return self.request('GET', '/ingredients')

    @allure.step('Создать заказ')
    def create_order(self, payload):
        return self.request('POST', '/orders', payload)

    @allure.step('Получить заказы пользователя')
    def orders(self):
        return self.request('GET', '/orders')
