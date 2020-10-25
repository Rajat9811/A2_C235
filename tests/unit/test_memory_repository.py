from datetime import date, datetime
from typing import List

import pytest

from movies.domain.model1 import Movie, Genre, Director, Actor, Review, make_review, User
from movies.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    user = User('wpking2', 'Alpha1234')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('wpking2') is user


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('wpking')
    assert user is None


def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_movies = in_memory_repo.get_number_of_movies()

    # Check that the query returned 6 Articles.
    assert number_of_movies == 1000


def test_repository_can_add_movie(in_memory_repo):
    movie = Movie(
        "17 Again",
        2020
    )
    in_memory_repo.add_movie(movie)
    assert in_memory_repo.get_movie(1001) is movie


def test_repository_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(2)
    # Check that the movie has the expected title.
    assert movie.title == '13 Hours'
    assert movie.genres == [Genre("Action"), Genre("Drama"), Genre("History")]
    assert movie.director == Director("Michael Bay")
    assert movie.actors == [Actor("John Krasinski"), Actor("Pablo Schreiber"), Actor("James Badge Dale"), Actor("David Denman")]
    assert movie.year == 2012
    assert len(movie.reviews) == 0

def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(9999)
    assert movie is None


def test_repository_can_retrieve_movies_by_year(in_memory_repo):
    movies = in_memory_repo.get_movies_by_year(2014)

    # Check that the query returned 98 movie_library.
    assert len(movies) == 98


def test_repository_does_not_retrieve_a_movie_when_there_are_no_movies_for_a_given_year(in_memory_repo):
    movies = in_memory_repo.get_movies_by_year(1800)
    assert len(movies) == 0


def test_repository_can_get_first_movie(in_memory_repo):
    movie = in_memory_repo.get_first_movie()
    assert movie.title == 'Guardians of the Galaxy'


def test_repository_can_get_last_movie(in_memory_repo):
    movie = in_memory_repo.get_last_movie()
    assert movie.title == 'Nine Lives'


def test_repository_can_get_movies_by_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([10, 45, 99])

    assert len(movies) == 3
    assert movies[
               0].title == 'Passengers'
    assert movies[1].title == "The Founder"
    assert movies[2].title == 'The Void'


def test_repository_does_not_retrieve_movie_for_non_existent_id(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([0, 2, 5000])

    assert len(movies) == 1
    assert movies[
               0].title == 'Prometheus'


def test_repository_returns_an_empty_list_for_non_existent_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([0, 5000])

    assert len(movies) == 0


def test_repository_returns_movie_ids_for_existing_actor(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_actor('Emma Watson')
    movie_ids.sort()
    assert movie_ids == [115, 236, 315, 419, 474, 555, 667, 719]


def test_repository_returns_an_empty_list_for_non_existent_actor(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_actor('yasuo')

    assert len(movie_ids) == 0

def test_repository_returns_movie_ids_for_existing_director(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_director('James Gray')
    movie_ids.sort()
    assert movie_ids == [9]


def test_repository_returns_an_empty_list_for_non_existent_director(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_director('yasuo')

    assert len(movie_ids) == 0

def test_repository_returns_an_empty_list_for_non_existent_genre(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_genre('gopher')

    assert len(movie_ids) == 0

def test_repository_can_add_a_review(in_memory_repo):
    user = User('spooky', 'Spookier9')
    in_memory_repo.add_user(user)
    user = in_memory_repo.get_user('spooky')
    movie = in_memory_repo.get_movie(2)
    review = make_review(review_text="This was pretty boring", user=user, movie= movie)

    in_memory_repo.add_review(review)

    assert review in in_memory_repo.get_reviews()


def test_repository_does_not_add_a_review_without_a_user(in_memory_repo):
    movie = in_memory_repo.get_movie(2)
    review = Review(None, movie, "Meh")

    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)


def test_repository_does_not_add_a_review_without_a_movie_properly_attached(in_memory_repo):
    user = User('spooky', 'Spookier9')
    in_memory_repo.add_user(user)
    user = in_memory_repo.get_user('Spooky')
    movie = in_memory_repo.get_movie(2)
    review = Review(None, movie, "Action packed!")

    user.add_review(review)

    with pytest.raises(RepositoryException):
        # Exception expected because the Article doesn't refer to the Comment.
        in_memory_repo.add_review(review)


def test_repository_can_retrieve_reviews(in_memory_repo):
    assert len(in_memory_repo.get_reviews()) == 0
    user = User('spooky', 'Spookier9')
    in_memory_repo.add_user(user)
    user = in_memory_repo.get_user('spooky')
    movie = in_memory_repo.get_movie(2)
    review = make_review(review_text="HIGHLY RECOMMEND!", user=user, movie=movie)

    in_memory_repo.add_review(review)
    assert len(in_memory_repo.get_reviews()) == 1


