from uuid import uuid4


def make_user():
    return {'email': f'valeriia_{uuid4().hex}@example.com',
            'password': f'Password_{uuid4().hex}', 'name': 'Valeriia'}


USER_EXISTS = {'success': False, 'message': 'User already exists'}
REQUIRED_FIELDS = {'success': False, 'message': 'Email, password and name are required fields'}
INVALID_CREDENTIALS = {'success': False, 'message': 'email or password are incorrect'}
UNAUTHORIZED = {'success': False, 'message': 'You should be authorised'}
NO_INGREDIENTS = {'success': False, 'message': 'Ingredient ids must be provided'}
