from strenum import StrEnum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class RoleEnum(StrEnum):
    user = "user"
    admin = "admin"


class UsersTable(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    user_name = Column(String(100))
    user_email = Column(String(100), unique=True, index=True)
    user_hashed_password = Column(String())
    user_role = Column(String, default=RoleEnum.user)
    user_created_at = Column(DateTime())
    user_updated_at = Column(DateTime())

    def dict(self):
        return {
            "user_email": self.user_email,
            "user_name": self.user_name,
            "user_hashed_password": self.user_hashed_password,
            "user_role": self.user_role,
            "user_created_at": self.user_created_at,
            "user_updated_at": self.user_updated_at,
        }


class KnowledgeBase(Base):
    __tablename__ = 'knowledge_base'

    id = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    file_name = Column(String)
    text = Column(String)
    image_paths = Column(String)
    created_at = Column(DateTime())

    def dict(self):
        return {
            "user_id": self.user_id,
            "file_name": self.file_name,
            "text": self.text,
            "image_paths": self.image_paths,
            "created_at": self.created_at,
        }

