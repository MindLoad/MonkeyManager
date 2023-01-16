""" Search service logic """

__all__ = ['SearchService']

from attrs import define
from sqlalchemy.orm.query import Query
from sqlalchemy import text
from sqlalchemy import or_
from models import Session, Passwords


@define(slots=True, frozen=True)
class SearchService:
    """ Search service dataclass """

    @classmethod
    def search(cls, phrase: str) -> Query:
        """
        Search logic
        :return: search results
        """
        phrase = f"%{phrase}%"
        sql = f"SELECT id, parent, child, title, login, email, url, phone, created, modified " \
              f"FROM passwords " \
              f"WHERE LOWER(title) LIKE LOWER(:phrase) OR LOWER(login) LIKE LOWER(:phrase) " \
              f"OR LOWER(email) LIKE LOWER(:phrase) OR LOWER(url) LIKE LOWER(:phrase) " \
              f"ORDER BY id ASC"
        with Session() as session:
            query = session.execute(text(sql), {'phrase': phrase})
        return query.fetchall()

    @classmethod
    def completer_search(cls, phrase: str) -> Query:
        """ Search with completer values """
        with Session() as session:
            query = session.query(Passwords).filter(
                or_(
                    Passwords.title == phrase,
                    Passwords.login == phrase
                )
            )
        return query.all()
