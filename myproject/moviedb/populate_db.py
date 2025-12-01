"""Utility script to seed the moviedb app with canonical movies.

Run with: python manage.py shell < moviedb/populate_db.py
"""
from __future__ import annotations

import os
import sys
from datetime import date
from pathlib import Path

import django
from django.db import transaction

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from moviedb.models import Director, Genre, Movie  # noqa: E402  pylint: disable=C0413

MOVIES = [
    {
        "title": "The Godfather",
        "pub_date": date(1972, 3, 24),
        "directors": [
            {"first_name": "Francis Ford", "last_name": "Coppola"},
        ],
        "genres": ["Crime", "Drama"],
        "description": "The aging patriarch of an organized crime dynasty transfers control to his reluctant son.",
    },
    {
        "title": "The Godfather Part II",
        "pub_date": date(1974, 12, 20),
        "directors": [
            {"first_name": "Francis Ford", "last_name": "Coppola"},
        ],
        "genres": ["Crime", "Drama"],
        "description": "Parallel stories follow young Vito Corleone's rise and Michael Corleone consolidating power.",
    },
    {
        "title": "The Shawshank Redemption",
        "pub_date": date(1994, 9, 23),
        "directors": [
            {"first_name": "Frank", "last_name": "Darabont"},
        ],
        "genres": ["Drama"],
        "description": "Two imprisoned men forge a deep bond that helps them find hope behind bars.",
    },
    {
        "title": "The Dark Knight",
        "pub_date": date(2008, 7, 18),
        "directors": [
            {"first_name": "Christopher", "last_name": "Nolan"},
        ],
        "genres": ["Action", "Crime", "Drama"],
        "description": "Batman faces the Joker's chaotic plans to push Gotham and its hero into anarchy.",
    },
    {
        "title": "Pulp Fiction",
        "pub_date": date(1994, 10, 14),
        "directors": [
            {"first_name": "Quentin", "last_name": "Tarantino"},
        ],
        "genres": ["Crime", "Drama"],
        "description": "Los Angeles crime stories intersect through witty dialogue and nonlinear storytelling.",
    },
    {
        "title": "Inception",
        "pub_date": date(2010, 7, 16),
        "directors": [
            {"first_name": "Christopher", "last_name": "Nolan"},
        ],
        "genres": ["Action", "Science Fiction", "Thriller"],
        "description": "A thief enters dreams to plant an idea in the mind of a powerful heir.",
    },
    {
        "title": "Schindler's List",
        "pub_date": date(1993, 12, 15),
        "directors": [
            {"first_name": "Steven", "last_name": "Spielberg"},
        ],
        "genres": ["Drama", "History", "War"],
        "description": "Oskar Schindler saves hundreds of Jewish refugees during World War II in Nazi-occupied Poland.",
    },
    {
        "title": "The Lord of the Rings: The Return of the King",
        "pub_date": date(2003, 12, 17),
        "directors": [
            {"first_name": "Peter", "last_name": "Jackson"},
        ],
        "genres": ["Adventure", "Fantasy"],
        "description": "Frodo and Sam reach Mount Doom while Aragorn claims his destiny to unite Middle-earth.",
    },
    {
        "title": "Fight Club",
        "pub_date": date(1999, 10, 15),
        "directors": [
            {"first_name": "David", "last_name": "Fincher"},
        ],
        "genres": ["Drama", "Thriller"],
        "description": "An insomniac office worker and a soap maker start an underground fight club that spirals.",
    },
    {
        "title": "Parasite",
        "pub_date": date(2019, 5, 30),
        "directors": [
            {"first_name": "Bong", "last_name": "Joon-ho"},
        ],
        "genres": ["Drama", "Thriller"],
        "description": "A poor Korean family schemes to infiltrate a wealthy household with unexpected consequences.",
    },
    {
        "title": "Spirited Away",
        "pub_date": date(2001, 7, 20),
        "directors": [
            {"first_name": "Hayao", "last_name": "Miyazaki"},
        ],
        "genres": ["Animation", "Fantasy"],
        "description": "A young girl is trapped in a spirit world and must work to free herself and her parents.",
    },
    {
        "title": "Interstellar",
        "pub_date": date(2014, 11, 7),
        "directors": [
            {"first_name": "Christopher", "last_name": "Nolan"},
        ],
        "genres": ["Adventure", "Science Fiction", "Drama"],
        "description": "Explorers travel through a wormhole seeking a new home for humanity as Earth collapses.",
    },
    {
        "title": "Mad Max: Fury Road",
        "pub_date": date(2015, 5, 15),
        "directors": [
            {"first_name": "George", "last_name": "Miller"},
        ],
        "genres": ["Action", "Adventure", "Science Fiction"],
        "description": "Furious desert chases erupt as Furiosa and Max flee a tyrant across the wasteland.",
    },
    {
        "title": "La La Land",
        "pub_date": date(2016, 12, 9),
        "directors": [
            {"first_name": "Damien", "last_name": "Chazelle"},
        ],
        "genres": ["Drama", "Romance", "Music"],
        "description": "A jazz musician and an aspiring actress pursue love while chasing their dreams in Los Angeles.",
    },
]


def _get_or_create_directors(directors_data):
    """Return Director instances for the provided payload."""
    directors = []
    for data in directors_data:
        director, _ = Director.objects.get_or_create(
            first_name=data["first_name"],
            last_name=data["last_name"],
        )
        directors.append(director)
    return directors


def _get_or_create_genres(genres_data):
    """Return Genre instances for the provided payload."""
    genres = []
    for name in genres_data:
        genre, _ = Genre.objects.get_or_create(name=name)
        genres.append(genre)
    return genres


def populate():
    """Populate the database with curated movies, directors, and genres."""
    summary = {
        "movies_created": 0,
        "movies_skipped": 0,
        "directors_created": 0,
        "genres_created": 0,
    }

    with transaction.atomic():
        for movie_data in MOVIES:
            directors = []
            for data in movie_data["directors"]:
                director, created = Director.objects.get_or_create(
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                )
                if created:
                    summary["directors_created"] += 1
                directors.append(director)

            genres = []
            for name in movie_data["genres"]:
                genre, created = Genre.objects.get_or_create(name=name)
                if created:
                    summary["genres_created"] += 1
                genres.append(genre)

            movie, created = Movie.objects.get_or_create(
                title=movie_data["title"],
                pub_date=movie_data["pub_date"],
                defaults={"description": movie_data["description"]},
            )

            if created:
                summary["movies_created"] += 1
            else:
                summary["movies_skipped"] += 1
                if movie.description != movie_data["description"]:
                    movie.description = movie_data["description"]
                    movie.save(update_fields=["description"])

            movie.directors.add(*directors)
            movie.genres.add(*genres)

    return summary


def run():
    summary = populate()
    print(
        "Movies created: {movies_created}, skipped: {movies_skipped}, new directors: {directors_created}, new genres: {genres_created}".format(
            **summary
        )
    )


if __name__ == "__main__":
    run()
