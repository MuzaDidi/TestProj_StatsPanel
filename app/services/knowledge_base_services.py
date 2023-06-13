from datetime import datetime
from io import BytesIO
import PyPDF2

from databases import Database
from fastapi import UploadFile, HTTPException, status
from sqlalchemy import insert
from db.models import KnowledgeBase
from schemas.knowledge_base_schemas import Knowledge, KnowledgeResult

import logging

logger = logging.getLogger(__name__)


class KnowledgeService:
    def __init__(self, db: Database):
        self.db = db

    async def process_pdf(self, file: UploadFile, user_id: int) -> KnowledgeResult:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file format. Only PDF files are supported."
            )

        pdf = PyPDF2.PdfReader(BytesIO(await file.read()))
        num_pages = len(pdf.pages)
        text = ""
        image_paths = []

        for page_number in range(num_pages):
            page = pdf.pages[page_number]
            text += page.extract_text()

            for image_file_object in page.images:
                image_filename = f"image_p{page_number + 1}_{image_file_object.name}"
                image_paths.append(image_filename)

        knowledge_base_create = Knowledge(
            user_id=user_id,
            file_name=file.filename,
            text=text,
            image_paths=str(image_paths),
            created_at=datetime.utcnow()
        )

        query_knowledge = insert(KnowledgeBase).values(**knowledge_base_create.dict()).returning(KnowledgeBase.id)
        knowledge_data = await self.db.fetch_one(query=query_knowledge)

        knowledge_result = KnowledgeResult(
            id=knowledge_data['id'],
            user_id=knowledge_base_create.user_id,
            file_name=knowledge_base_create.file_name,
            text=knowledge_base_create.text,
            image_paths=knowledge_base_create.image_paths,
            created_at=knowledge_base_create.created_at
        )

        logger.info(f"PDF file saved with id: {knowledge_result.id}")
        return knowledge_result
