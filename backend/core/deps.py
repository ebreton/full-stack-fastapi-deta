from deta import Base, Deta

from core.config import settings

RESUSABLE_DB = None


def get_db() -> Base:
    global RESUSABLE_DB
    if RESUSABLE_DB is None:
        RESUSABLE_DB = Deta(settings.PROJECT_KEY).Base(settings.DB_NAME)
    return RESUSABLE_DB
