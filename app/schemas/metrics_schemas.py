from datetime import datetime
from strenum import StrEnum

from pydantic import BaseModel


class FeedbackEnum(StrEnum):
    positive = "positive"
    negative = "negative"


class Conversation(BaseModel):
    user_id: int
    duration: int  # in seconds
    feedback: FeedbackEnum
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


class TotalEscalations(BaseModel):
    result: list[Escalation]


class SatisfactionPercentage(BaseModel):
    positive: float
    negative: float


class SatisfactionResponse(BaseModel):
    result: SatisfactionPercentage

