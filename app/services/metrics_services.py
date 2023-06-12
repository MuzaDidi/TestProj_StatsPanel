from databases import Database
from schemas.users_schemas import *
from db import data_mock

import logging

logger = logging.getLogger(__name__)


class MetricService:
    def __init__(self, db: Database):
        self.db = db

    async def get_average_conversation_time(self, start_date: datetime, end_date: datetime) -> float:
        get_conversations = [
            conversation for conversation in data_mock.conversations
            if start_date <= conversation.created_at <= end_date
        ]
        total_duration = sum(
            conversation.duration for conversation in get_conversations)
        total_conversations = len(get_conversations)
        average_time = total_duration / total_conversations if total_conversations > 0 else 0
        return average_time

    async def get_total_conversation_number(self) -> int:
        total_conversations = len(data_mock.conversations)
        return total_conversations

    async def get_total_conversation_number_for_subset(self, user_ids: list[int]) -> int:
        total_conversations = 0
        for conversation in data_mock.conversations:
            if conversation.user_id in user_ids:
                total_conversations += 1
        return total_conversations

