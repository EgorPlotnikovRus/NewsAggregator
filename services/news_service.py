from api.schemas import NewsArticle
from models.news import NewsArticleDB
from models.database import get_db

def save_articles(articles: list[NewsArticle]):
    db = next(get_db())
    for article in articles:
        existing_article = db.query(NewsArticleDB).filter(NewsArticleDB.title == article.title).first()
        if not existing_article:
            db_article = NewsArticleDB(
                title=article.title,
                pub_date=article.pub_date,
                category=article.category,
                link=article.link,
                resurse_name=article.resurse_name,
                content=article.content
            )
            db.add(db_article)
    db.commit()