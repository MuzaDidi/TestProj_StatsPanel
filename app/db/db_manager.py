from databases import Database
from core.system_config import db_url


db = Database(db_url)


def get_db():
    return db
