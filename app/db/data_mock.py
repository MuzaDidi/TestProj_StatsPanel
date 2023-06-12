from datetime import datetime
from schemas.metrics_schemas import Conversation, Escalation, FeedbackEnum

conversations = [
    Conversation(user_id=3, duration=300, feedback=FeedbackEnum.negative.value, created_at=datetime(2023, 6, 1, 18, 0, 0)),
    Conversation(user_id=2, duration=120, feedback=FeedbackEnum.positive.value, created_at=datetime(2023, 6, 1, 10, 0, 0)),
    Conversation(user_id=1, duration=180, feedback=FeedbackEnum.negative.value, created_at=datetime(2023, 6, 1, 11, 0, 0)),
    Conversation(user_id=3, duration=90, feedback=FeedbackEnum.positive.value, created_at=datetime(2023, 6, 2, 9, 0, 0)),
    Conversation(user_id=2, duration=155, feedback=FeedbackEnum.positive.value, created_at=datetime(2023, 6, 3, 9, 32, 0)),
]


escalations = [
    Escalation(description="escalation 1"),
    Escalation(description="escalation 2")
]
