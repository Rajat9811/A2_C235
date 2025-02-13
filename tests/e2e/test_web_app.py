import pytest

from flask import session

from movies.authentication.services import AuthenticationException
from movies.movie_library import services as movie_library_services
from movies.authentication import services as auth_services
from movies.movie_library.services import NonExistentMovieException
from movies.domain.model1 import Movie, Genre, Director, Actor, Review, User

def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid username and password.
    response = client.post(
        '/authentication/register',
        data={'username': 'spooky', 'password': 'Spookier9'}
    )

    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Your username is required'),
        ('cj', '', b'Your username is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must at least 8 characters, and contain an upper case letter, a lower case letter and a digit'),
        ('spooky', 'Test#6^0', b'Your username is already taken - please supply another'),
))


def test_register_with_invalid_input(client, username, password, message):
    client.post(
        '/authentication/register',
        data={'username': 'spooky', 'password': 'spooky'}
    )


    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data



def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'!K Movie Database' in response.data


def test_login_required_to_comment(client):
    response = client.post('/review')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_movies_without_rank(client):
    # Check that we can retrieve the movies page.
    response = client.get('/movies_by_rank')
    assert response.status_code == 200

    # Check that without providing a rank query parameter the page includes the first movie.
    assert b'Nitesh Tiwari' in response.data
    assert b'Dangal' in response.data


def test_movies_with_rank(client):
    # Check that we can retrieve the articles page.
    response = client.get('/movies_by_rank?id=21')

    assert response.status_code == 200

    # Check that all articles on the requested date are included on the page.
    assert b'Stephen Gaghan' in response.data
    assert b'Gold' in response.data


def test_movies_with_genre(client):
    # Check that we can retrieve the movies page.
    response = client.get('/movies_by_genre?genre=Action')
    assert response.status_code == 200

    assert b'Action Movies' in response.data
    assert b'Guardians of the Galaxy' in response.data
