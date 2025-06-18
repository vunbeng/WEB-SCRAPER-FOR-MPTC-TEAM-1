from sqlalchemy.orm import sessionmaker
from database.models import Article, engine

Session = sessionmaker(bind=engine)
session = Session()

def create_entry(url, khmer_texts, english_texts):
    article = Article(url=url, khmer_texts=khmer_texts, english_texts=english_texts)

    session.add(article)
    session.commit()