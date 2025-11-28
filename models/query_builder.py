""" SQL Query Builder """

__all__ = ['QueryBuilder']

from attrs import define

from models import Passwords, Session


@define(slots=True)
class QueryBuilder:
    """ SQL Query Builder """

    @classmethod
    def delete_obj(cls, row_id: int) -> None:
        """ Delete object by row_id """
        with Session() as session:
            obj = session.query(Passwords).where(Passwords.id == row_id).first()
            session.delete(obj)
            session.commit()

    @classmethod
    def retrieve_parents(cls, root_parent: str) -> list:
        """ Retrieve parents """
        with Session() as session:
            query = session.query(Passwords.child).where(
                Passwords.parent == root_parent
            ).order_by(Passwords.child.asc()).distinct(Passwords.child)
        return query

    @classmethod
    def retrieve_children(cls, parent: str) -> list:
        """ Retrieve parent children """
        with Session() as session:
            query = session.query(Passwords).where(
                Passwords.child == parent
            ).order_by(Passwords.title.asc()).all()
        return query

    @classmethod
    def create_item(cls, **kwargs) -> None:
        """ Create new item """
        with Session() as session:
            session.execute(
                Passwords.__table__.insert().values(**kwargs)
            )
            session.commit()

    @classmethod
    def update_item(
            cls, item_id: int, title: str, login: str, email: str, password: bytes, url: str, phone: str,
            modified: str
    ) -> None:
        """ Update item """
        with Session() as session:
            obj = session.query(Passwords).where(Passwords.id == item_id).first()
            obj.title = title
            obj.login = login
            obj.email = email
            obj.password = password
            obj.url = url
            obj.phone = phone
            obj.modified = modified
            session.commit()

    @classmethod
    def retrieve_item_password(cls, item_id: int) -> Passwords:
        """ Retrieve item """
        with Session() as session:
            query = session.query(Passwords.password).where(Passwords.id == item_id).first()
        return query

    @classmethod
    def completer_values(cls) -> list:
        """ Retrieve value for search auto completer """
        with Session() as session:
            query = session.query(Passwords.title, Passwords.login).all()
        return [
            *(each[0] for each in query),
            *(each[1] for each in query)
        ]

    @classmethod
    def count_parents(cls, title: str) -> int:
        """ Count parent by title """
        with Session() as session:
            query = session.query(Passwords).where(Passwords.parent == title).count()
        return query
