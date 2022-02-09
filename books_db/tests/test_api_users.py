from flask import url_for

from data import db
from users.models import User


def test_get_users_no_related(anonymous_client, test_user1):
    url_users = url_for('api.get_users')
    url_one_user = url_for('api.get_user', user_id=test_user1.id)

    valid_response = {
        "email": test_user1.email,
        "id": test_user1.id,
        "username": test_user1.username
    }

    response = anonymous_client.get(url_users)
    assert response.status_code == 200
    assert response.status_code != 404, f'Endpoint `{url_users}` not found'
    assert response.json == [valid_response], (
        f'Check is GET request to `{url_users}` returns right response'
    )

    response = anonymous_client.get(url_one_user)
    assert response.status_code == 200
    assert response.status_code != 404, f'Endpoint `{url_users}` not found'
    assert response.json == valid_response, (
        f'Check is GET request to `{url_users}` returns right response'
    )


def test_get_users_with_related(anonymous_client, test_user1,
                                test_book1, test_author1):
    url_users = url_for('api.get_users', with_authors=True, with_books=True)
    url_one_user = url_for(
        'api.get_user', user_id=test_user1.id,
        with_authors=True, with_books=True,
    )

    valid_response = {
        "authors": [
            {
                "created": test_author1.created.strftime(
                    '%Y-%m-%d %H:%M:%S'
                ),
                "fio": test_author1.fio,
                "id": test_author1.id,
                "isbn": test_author1.isbn
            }
        ],
        "books": [
            {
                "created": test_book1.created.strftime(
                    '%Y-%m-%d %H:%M:%S'
                ),
                "id": test_book1.id,
                "isbn": test_book1.isbn,
                "number_of_pages": test_book1.number_of_pages,
                "review": test_book1.review,
                "title": test_book1.title
            }
        ],
        "email": test_user1.email,
        "id": test_user1.id,
        "username": test_user1.username
    }

    response = anonymous_client.get(url_users)
    assert response.status_code == 200
    assert response.status_code != 404, f'Endpoint `{url_users}` not found'
    assert response.json == [valid_response], (
        f'Check is GET request to `{url_users}` returns right response'
    )

    response = anonymous_client.get(url_one_user)
    assert response.status_code == 200
    assert response.status_code != 404, f'Endpoint `{url_users}` not found'
    assert response.json == valid_response, (
        f'Check is GET request to `{url_users}` returns right response'
    )


def test_post_users(anonymous_client, test_user1):
    url = url_for('api.create_user')
    empty_data = {}
    user_count_before = db.session.query(User).count()

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
    user_count_after = db.session.query(User).count()
    assert user_count_before < user_count_after, (
        f'Check if POST request to `{url}` creates user.'
    )


def test_update_user_anonymous(anonymous_client, test_user1):
    url = url_for('api.update_user', user_id=test_user1.id)
    assert anonymous_client.put(url).status_code == 401, (
        f'Check if PUT request to `{url}` is available only for authorized'
    )


# def test_update_another_user(authorized_client, test_user2):
#     url = url_for('api.update_user', user_id=test_user2.id)
#     assert authorized_client.put(url).status_code == 403, (
#         f'Check if PUT request to `{url}` is available only for authorized'
#     )
