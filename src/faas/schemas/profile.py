from pydantic import BaseModel, Field


class ProfileResponse(BaseModel):
    user_id: str = Field(strict=True)
