from fastapi import APIRouter, HTTPException, status, Depends, Query
from databases import Database
from db.db_manager import get_db
from db.models import RoleEnum
from schemas import metrics_schemas
from schemas.users_schemas import User
from services.metrics_services import MetricService
from services.user_service import UserService
from routers.depends import get_current_user
from schemas.metrics_schemas import *

router = APIRouter(tags=['Metrics'],)


@router.get('/metrics/average_conversation_time/', response_model=metrics_schemas.AvgConversationTime,
            dependencies=[Depends(get_current_user)], status_code=200)
async def get_average_conversation_time(start_date: str = "2023-06-01T16:19:43", end_date: str = "2023-06-03T16:19:43",
                                        db: Database = Depends(get_db)) -> AvgConversationTime:
    metric_service = MetricService(db=db)
    start_date = datetime.fromisoformat(start_date)
    end_date = datetime.fromisoformat(end_date)

    result = await metric_service.get_average_conversation_time(start_date=start_date, end_date=end_date)
    return AvgConversationTime(result=result)


@router.get('/metrics/total_conversation_number/', response_model=metrics_schemas.TotalConversationNumber,
            dependencies=[Depends(get_current_user)], status_code=200)
async def get_total_conversation_number(db: Database = Depends(get_db)) -> TotalConversationNumber:
    metric_service = MetricService(db=db)

    result = await metric_service.get_total_conversation_number()
    return TotalConversationNumber(result=result)


@router.get('/metrics/total_conversation_number_for_subset/',
            response_model=metrics_schemas.TotalConversationNumber, status_code=200)
async def get_total_conversation_number_for_subset(user_ids: list[int] = Query(..., description="List of user IDs"),
                                                   current_user: User = Depends(get_current_user),
                                                   db: Database = Depends(get_db)) -> TotalConversationNumber:
    metric_service = MetricService(db=db)
    user_service = UserService(db=db)

    if current_user.user_role != RoleEnum.admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Only admins have access.')

    is_user_exist = [await user_service.get_user_by_id(user_id=user_id) for user_id in user_ids]

    result = await metric_service.get_total_conversation_number_for_subset(user_ids=user_ids)
    return TotalConversationNumber(result=result)
