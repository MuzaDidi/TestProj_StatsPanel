from datetime import datetime
from schemas.metrics_schemas import Conversation


conversations = [
    Conversation(user_id=3, duration=300, created_at=datetime(2023, 6, 1, 18, 0, 0)),
    Conversation(user_id=3, duration=120, created_at=datetime(2023, 6, 1, 10, 0, 0)),
    Conversation(user_id=4, duration=180, created_at=datetime(2023, 6, 1, 11, 0, 0)),
    Conversation(user_id=3, duration=90, created_at=datetime(2023, 6, 2, 9, 0, 0)),
]

