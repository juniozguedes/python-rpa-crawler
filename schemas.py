from pydantic import BaseModel
from typing import List


class NewsRequest(BaseModel):
    search_phrase: str
    news_category: List[str]
    months: int
