from sqlmodel import SQLModel
from .db import engine


def init_db():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
    print("DB tables created.")
