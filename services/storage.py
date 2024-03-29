""" Database export service """

__all__ = ['ExportService']

import json
import chime
from attrs import define
from pathlib import Path
from loguru import logger
from models import Passwords, Session
from tools import run_decode

logger.add(
    Path(__file__).cwd() / 'logs/errors.log',
    rotation="1 MB",
    compression="zip",
    format="<green>{time}</green> {level} <level>{message}</level>"
)


@define(slots=True)
class ExportService:
    """ Export service """

    @classmethod
    def decode_password_field(cls, key: str, password: bytes) -> str:
        """ Decode password """
        try:
            return run_decode(key, password).decode("utf-8")
        except UnicodeDecodeError:
            logger.error(f'Error while decrypt password / key: {key}')
            return 'Invalid'

    @classmethod
    def make_export(cls, key: str) -> None:
        """ Export sqlite3 database to file with SQL statements """

        if not key.strip():
            chime.error()
            return

        with Session() as session:
            elements = json.dumps(
                [{
                    "id": each.id,
                    "parent": each.parent,
                    "child": each.child,
                    "title": each.title,
                    "login": each.login,
                    "email": each.login,
                    "password": cls.decode_password_field(key=key, password=each.password),
                    "url": each.url,
                    "created": each.created,
                    "modified": each.modified
                } for each in session.query(Passwords)],
                indent=2
            )

        with open('export.json', 'w') as outfile:
            outfile.write(elements)

        chime.success()
