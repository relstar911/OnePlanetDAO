from sqlmodel import Session, create_engine

from .config import DATABASE_URL, ENVIRONMENT

_connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    _connect_args["check_same_thread"] = False

engine = create_engine(
    DATABASE_URL,
    echo=(ENVIRONMENT == "development"),
    connect_args=_connect_args,
)


def get_session():
    with Session(engine) as session:
        yield session
