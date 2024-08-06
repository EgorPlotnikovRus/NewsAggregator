from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class NewsArticleDB(Base):
    __tablename__ = 'news_articles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    pub_date = Column(DateTime)
    category = Column(String)
    link = Column(String)
    resurse_name = Column(String)
    content = Column(String)