from fastapi import FastAPI, Query, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from services.parser import Parser
import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from models.database import get_db
from models.news import NewsArticleDB
from fastapi.templating import Jinja2Templates
import asyncio



app = FastAPI()
scheduler = BackgroundScheduler()

templates = Jinja2Templates(directory="templates")


async def scheduled_job():
    print('Parsing.....')
    parser = Parser()
    await asyncio.to_thread(parser.parse)
    await asyncio.to_thread(parser.save_articles_to_db)


def start_scheduled_job():
    asyncio.create_task(scheduled_job())


@app.on_event("startup")
def start_scheduler():
    start_scheduled_job()

    scheduler.add_job(start_scheduled_job, 'interval', minutes=60 * 24)
    scheduler.start()


@app.get("/", response_class=HTMLResponse)
async def read_articles(request: Request, skip: int = Query(0), limit: int = Query(30)):
    db = next(get_db())
    articles = db.query(NewsArticleDB).offset(skip).limit(limit).all()

    return templates.TemplateResponse("test.html", {"request": request, "articles": articles})


@app.get("/news/{news_id}", response_class=HTMLResponse)
async def read_news(news_id: int, request: Request):
    db = next(get_db())
    news_item = db.query(NewsArticleDB).filter(NewsArticleDB.id == news_id).first()

    if news_item is None:
        raise HTTPException(status_code=404, detail="News not found")

    return templates.TemplateResponse("news_detail.html", {"request": request, "news_item": news_item})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
