from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

db_url = "sqlite:///database/database.db"

engine = create_engine(db_url, echo=True)

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    summary = Column(String)
    url = Column(String)

Base.metadata.create_all(engine)