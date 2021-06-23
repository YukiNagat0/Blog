import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session, declarative_base


SqlAlchemyBase = declarative_base()

__factory = None


def global_init(db_file: str):
    global __factory

    if __factory:
        raise Exception('База данных уже инициализирована.')

    if not db_file or not db_file.strip():
        raise Exception('Необходимо указать файл базы данных.')

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory

    return __factory()
