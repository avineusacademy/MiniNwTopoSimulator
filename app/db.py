from sqlmodel import SQLModel, Session, create_engine

engine = create_engine("sqlite:///network.db")

def init_db():
    SQLModel.metadata.create_all(engine)
