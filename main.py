from fastapi import FastAPI, Query, Depends, Request
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from services.parser import Parser
import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from models.database import get_db
from models.news import NewsArticleDB
from fastapi.templating import Jinja2Templates


app = FastAPI()
scheduler = BackgroundScheduler()

templates = Jinja2Templates(directory="templates")


def scheduled_job():
    print('Parsing.....')
    parser = Parser()
    parser.parse()
    parser.save_articles_to_db()

@app.on_event("startup")
def start_scheduler():
    scheduled_job()

    scheduler.add_job(scheduled_job, 'interval', minutes=60*24)
    scheduler.start()

from models.database import SessionLocal
@app.get("/", response_class=HTMLResponse)
async def read_articles(request: Request, skip: int = Query(0), limit: int = Query(30)):
    db = next(get_db())
    articles = db.query(NewsArticleDB).offset(skip).limit(limit).all()

    return templates.TemplateResponse("test.html", {"request": request, "articles": articles})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
