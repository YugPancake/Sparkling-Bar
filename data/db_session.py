import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
from contextlib import contextmanager

SqlAlchemyBase = dec.declarative_base()

__factory = None

def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    # Настройки пула соединений
    engine = sa.create_engine(
        conn_str,
        echo=False,
        pool_size=10,          # Количество постоянных соединений
        max_overflow=20,       # Максимальное количество временных соединений
        pool_timeout=30,       # Время ожидания соединения (сек)
        pool_pre_ping=True,    # Проверка активности соединения перед использованием
        pool_recycle=3600      # Пересоздавать соединения каждые 3600 секунд (1 час)
    )
    
    __factory = orm.sessionmaker(bind=engine, expire_on_commit=False)

    from . import _all_models

    SqlAlchemyBase.metadata.create_all(engine)

def create_session() -> Session:
    global __factory
    if not __factory:
        raise RuntimeError("Сначала вызовите global_init()")
    return __factory()

@contextmanager
def session_scope():
    """Контекстный менеджер для автоматического управления сессиями"""
    session = create_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()