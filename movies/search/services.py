from movies.adapters.repository import AbstractRepository
from movies.domain.hub import Actor, Director, Genre

def search_exists(search, select, repo: AbstractRepository):

    if select == "Actor":
        if Actor(search) in repo.get_actors():
            return True
        else:
            return False
    elif select == "Genre":
        if Genre(search) in repo.get_genres():
            return True
        else:
            return False
    elif select == "Director":
        if Director(search) in repo.get_directors():
            return True
        else:
            return False
