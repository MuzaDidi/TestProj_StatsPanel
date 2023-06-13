from datetime import datetime

from pydantic import BaseModel


class Knowledge(BaseModel):
    user_id: int
    file_name: str
    text: str
    image_paths: str
    created_at: datetime


class KnowledgeResult(Knowledge):
    id: int
