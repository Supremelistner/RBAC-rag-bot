from pydantic import BaseModel

class RAGQuery(BaseModel):
    question: str
