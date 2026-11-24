import pytest

from api.stellar_api import StellarApi
from data import make_user


@pytest.fixture
def api():
    client = StellarApi()
    yield client
    client.close()


@pytest.fixture
def user_factory(api):
    tokens = []

    def create(payload):
        response = api.register(payload)
        if response.ok and response.json().get('accessToken'):
            tokens.append(response.json()['accessToken'])
        return response

    yield create
    for token in tokens:
        client = StellarApi(token)
        try:
            client.delete_user().raise_for_status()
        finally:
            client.close()


@pytest.fixture
def user_data():
    return make_user()


@pytest.fixture
def registered_user(user_factory, user_data):
    response = user_factory(user_data)
    response.raise_for_status()
    return {**user_data, 'token': response.json()['accessToken']}


@pytest.fixture
def authorized_api(registered_user):
    client = StellarApi(registered_user['token'])
    yield client
    client.close()


@pytest.fixture
def ingredient_ids(api):
    response = api.ingredients()
    response.raise_for_status()
    ingredients = response.json()['data']
    bun = next(item['_id'] for item in ingredients if item['type'] == 'bun')
    filling = next(item['_id'] for item in ingredients if item['type'] == 'main')
    return [bun, filling, bun]


@pytest.fixture
def own_order(authorized_api, ingredient_ids):
    response = authorized_api.create_order({'ingredients': ingredient_ids})
    response.raise_for_status()
    return response.json()['order']


@pytest.fixture
def another_users_order(user_factory, ingredient_ids):
    response = user_factory(make_user())
    response.raise_for_status()
    client = StellarApi(response.json()['accessToken'])
    try:
        order = client.create_order({'ingredients': ingredient_ids})
        order.raise_for_status()
        return order.json()['order']
    finally:
        client.close()
