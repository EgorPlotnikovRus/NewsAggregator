from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NewsArticle(BaseModel):
    title: str
    pub_date: datetime
    category: Optional[str]
    link: str
    resurse_name: str
    content: Optional[str]