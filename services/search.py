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

    def search(
            self,
            phrase: str,
    ) -> typing.Union[Cursor, None]:
        """
        Search logic
        :return: sql query (search results)
        """

        phrase = phrase.strip().replace('*', '%')

        if phrase:
            sql = "SELECT id, title, login, email, url, phone, created, modified " \
                  "FROM passwords " \
                  "WHERE LOWER(title) LIKE LOWER(:search_line) OR LOWER(login) LIKE LOWER(:search_line) " \
                  "OR LOWER(email) LIKE LOWER(:search_line) OR LOWER(url) LIKE LOWER(:search_line) " \
                  "ORDER BY id ASC"
            query = self.cursor.execute(
                sql, {"search_line": phrase}
            )
            return query
        return None
