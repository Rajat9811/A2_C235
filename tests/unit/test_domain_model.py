from datetime import date

from movies.domain.hub import Movie, Genre, Director, Actor, Review, make_review, User

import pytest


@pytest.fixture()
def movie():
    return Movie(
        "War Dogs",
        2016
    )


@pytest.fixture()
def user():
    return User('spooky', 'Spookier9')


@pytest.fixture()
def actor():
    return Actor('Jonah Hill')

@pytest.fixture()
def genre():
    return Genre('Comedy')

@pytest.fixture()
def director():
    return Director('James Bobin')


def test_user_construction(user):
    assert user.username == 'spooky'
    assert user.password == 'Spookier9'
    assert repr(user) == '<User spooky Spookier9>'

    for review in user.reviews:
        # User should have an empty list of reviews after construction.
        assert False


def test_movie_construction(movie):
    assert movie.id is None
    assert movie.year == 2014
    assert movie.title == 'War Dogs'

    assert len(movie.reviews) == 0
    assert len(movie.actors) == 0
    assert len(movie.genres) == 0
    assert movie.director is None

    assert repr(movie) == '<War Dogs, 2016>'


def test_article_less_than_operator(movie):
    movie1 = Movie(
        "Boyo",
        None
    )

    movie2 = Movie(
        'War Dogs',
        2020
    )

    assert movie1 < movie
    assert movie < movie2


def test_actor_construction(actor):
    assert actor.actor_full_name == 'Lily James'

    for colleague in actor.colleagues:
        assert False


def test_make_review_establishes_relationships(movie, user):
    review_text = 'terrible movie'
    #rating = 1
    review = make_review(review_text=review_text, user=user, movie=movie)

    # Check that the User object knows about the review.
    assert review in user.reviews

    # Check that the review knows about the User.
    assert review.user is user

    # Check that movie knows about the review.
    assert review in movie.reviews

    # Check that the review knows about the movie.
    assert review.movie is movie


