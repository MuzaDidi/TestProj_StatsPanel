from datetime import datetime
from pydantic import BaseModel


class Conversation(BaseModel):
    user_id: int
    duration: int  # in seconds
    created_at: datetime


class Escalation(BaseModel):
    description: str


class TimeSpan(BaseModel):
    start_date: str
    end_date: str


class AvgConversationTime(BaseModel):
    result: float


class TotalConversationNumber(BaseModel):
    result: int
