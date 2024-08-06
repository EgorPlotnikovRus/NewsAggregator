from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from services.parser import Parser
import uvicorn
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()
scheduler = BackgroundScheduler()

app.mount("/static", StaticFiles(directory="static"), name="static")

HTML_FILE_PATH = "static/test.html"

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

@app.get("/", response_class=HTMLResponse)
async def read_html():
    with open(HTML_FILE_PATH, "r", encoding="utf-8") as file:
        page = file.read()
    return HTMLResponse(content=page)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
