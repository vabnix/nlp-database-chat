from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Query(BaseModel):
    text: str

class QueryResult(BaseModel):
    sql_query: str
    results: List[dict]
    execution_time: float