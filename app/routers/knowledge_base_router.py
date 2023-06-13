from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from databases import Database

from db.db_manager import get_db
from db.models import RoleEnum
from services.knowledge_base_services import KnowledgeService
from schemas.users_schemas import User
from routers.depends import get_current_user
from schemas.knowledge_base_schemas import KnowledgeResult

router = APIRouter(tags=['KnowledgeBase'],)


@router.post("/knowledge_base/upload_pdf/", response_model=KnowledgeResult, status_code=200)
async def extract_text_from_pdf(file: UploadFile = File(), db: Database = Depends(get_db),
                                current_user: User = Depends(get_current_user)) -> KnowledgeResult:
    knowledge_base_service = KnowledgeService(db=db)
    if current_user.user_role != RoleEnum.admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Only admins have an access.')
    result = await knowledge_base_service.process_pdf(file=file, user_id=current_user.user_id)
    return result
