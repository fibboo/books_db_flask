from users.models import User


def test_get_users(anonymous_client):
    url = '/api/users'
    response = anonymous_client.get(url)
    assert response.status_code == 200
    assert response.status_code != 404, f'Endpoint `{url}` not found'


def test_post_users(anonymous_client):
    url = '/api/users'
    empty_data = {}
    response = anonymous_client.post(url, json=empty_data)
    assert response.status_code == 400, (
        f'Check if POST request to `{url}` with empty data returns 400'
    )
    no_email_data = {
        'username': 'TestUser_noemail',
        'password': 'password_noemail'
    }
    response = anonymous_client.post(url, json=no_email_data)
    assert response.status_code == 400, (
        f'Check if POST request to `{url}` with no email returns 400'
    )
    test_user1 = User.create(
        username='TestUser1', email='testuser1@books.db', password='1234567',
    )
    duplicate_email = {
        'username': 'TestUser_duplicate',
        'password': 'password_duplicate',
        'email': test_user1.email
    }
    response = anonymous_client.post(url, json=duplicate_email)
    assert response.status_code == 400, (
        f'Check if POST request to `{url}` with existing email returns 400'
    )
    duplicate_username = {
        'username': test_user1.username,
        'password': 'password_duplicate',
        'email': 'test-dublicate@book.db'
    }
    response = anonymous_client.post(url, json=duplicate_username)
    assert response.status_code == 400, (
        f'Check if POST request to `{url}` with existing username returns 400'
    )
    valid_data = {
        'username': 'TestUser_777',
        'password': '123456789',
        'email': 'TestUser-777@book.db'
    }
    response = anonymous_client.post(url, json=valid_data)
    assert response.status_code == 201, (
        f'Check if POST request to `{url}` with valid data returns 201'
    )
    data = {
        'email': 'TestUser-777@book.db',
        'id': 2,
        'username': 'TestUser_777'
    }
    response_data = response.json
    assert response_data.get('email') == data['email'], (
        f'Check if POST request to `{url}` with valid data returns `email`.'
    )
    assert response_data.get('id') == data['id'], (
        f'Check if POST request to `{url}` with valid data returns `id`.'
    )
    assert response_data.get('username') == data['username'], (
        f'Check if POST request to `{url}` with valid data returns `username`.'
    )

