import sqlite3
from pathlib import Path

from flask import g

DATABASE = Path(__file__).parent.parent / "database" / "profanities.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(str(DATABASE))
        g.db.row_factory = sqlite3.Row
    return g.db
