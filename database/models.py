from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

db_url = "sqlite:///database/database.db"

engine = create_engine(db_url, echo=True)

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    khmer_texts = Column(String)
    english_texts = Column(String)

Base.metadata.create_all(engine)