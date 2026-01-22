from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from service_config import settings

DATABASE_URL = settings.db_url

engine = create_engine(url=DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_db() -> SessionLocal:
    """
    Генератор для получения сесси БД
    :return:
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
