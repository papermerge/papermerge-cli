from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    home_folder_id: UUID
    inbox_folder_id: UUID
