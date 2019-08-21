"""
Search service logic
"""

__all__ = [
    'SearchService',
]

import typing

from dataclasses import dataclass
from sqlite3 import Cursor


@dataclass
class SearchService:
    """
    Search service dataclass
    """

    cursor: Cursor
    phrase: str

    def __post_init__(self):
        """
        Prepare search phrase for sql query
        :return: search phrase
        """

        self.phrase = self.phrase.strip().replace('*', '%')

    def search(self) -> typing.Union[Cursor, None]:
        """
        Search logic
        :return: sql query (search results)
        """

        if self.phrase:
            sql = "SELECT id, title, login, email, url, phone, created, modified " \
                  "FROM passwords " \
                  "WHERE LOWER(title) LIKE LOWER(:search_line) OR LOWER(login) LIKE LOWER(:search_line) " \
                  "OR LOWER(email) LIKE LOWER(:search_line) OR LOWER(url) LIKE LOWER(:search_line) " \
                  "ORDER BY id ASC"
            query = self.cursor.execute(
                sql, {"search_line": self.phrase}
            )
            return query
        return None
