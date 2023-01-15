""" Search service logic """

__all__ = ['SearchService']

from sqlalchemy.orm.query import Query
from sqlalchemy import text
from models import session


class SearchService:
    """ Search service dataclass """

    @classmethod
    def search(cls, phrase: str) -> Query:
        """
        Search logic
        :return: search results
        """
        phrase = f"%{phrase}%"
        sql = f"SELECT id, title, login, email, url, phone, created, modified " \
              f"FROM passwords " \
              f"WHERE LOWER(title) LIKE LOWER(:phrase) OR LOWER(login) LIKE LOWER(:phrase) " \
              f"OR LOWER(email) LIKE LOWER(:phrase) OR LOWER(url) LIKE LOWER(:phrase) " \
              f"ORDER BY id ASC"
        return session.execute(text(sql), {'phrase': phrase}).fetchall()
